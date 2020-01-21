import uuid
import os
import time
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import pymongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["SECRET_KEY"] = "Nmr_JMruq7stpCsuYsGidA"

MONGODB_URI = os.getenv("MONGO_URI")
DBS_NAME = "terming_for_learning"
TERMS = "terms"
CATEGORIES = "categories"
USERS = "users"
SAVED = "saved"


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to Mongo: {}".format(e))


conn = mongo_connect(MONGODB_URI)
terms = conn[DBS_NAME][TERMS]
categories = conn[DBS_NAME][CATEGORIES]
users = conn[DBS_NAME][USERS]
saved = conn[DBS_NAME][SAVED]


# Helper functions
def check_session_user(session):
    if session.get("USERNAME", None) is not None:
        username = session["USERNAME"]
    return username


def liked(term_id, user):
    if term_id in user["liked"]:
        return True
    else:
        return False


def num_of_likes(term_id, coll):
    likes_array = []
    num_of_instances = coll.find({"liked": term_id})

    for term_id in num_of_instances:
        likes_array.append(term_id)

    return len(likes_array)

# Home screen / main welcome page:
@app.route("/")
def welcome():
    return render_template("home.html")

# User login:
@app.route("/user_login")
def user_login():
    return render_template("user_login.html")

# User sign-out:
@app.route("/sign_out")
def sign_out():
    session.pop("USERNAME", None)

    return redirect(url_for("welcome"))

# Delete profile request:
@app.route("/delete_profile_request/<user_id>")
def delete_profile_request(user_id):
    user = users.find_one({"_id": ObjectId(user_id)})

    return render_template("delete_profile_request.html", user=user,
                           saved_terms=saved
                           .find({"saved_by": user["username"]}))

# Delete profile:
@app.route("/delete_profile/<user_id>")
def delete_profile(user_id):
    username = check_session_user(session)

    user = users.find_one({"_id": ObjectId(user_id)})
    users.delete_one(user)
    session.pop("USERNAME", None)

    categories.delete_many({"author": username})
    terms.delete_many({"author": username})

    return redirect(url_for("welcome"))

# checks the login credentials and loads the terms list:
@app.route("/valid_login", methods=["POST"])
def valid_login():
    email = request.form["email"]
    password = request.form["password"]
    user_exists = users.find_one({"email": email})

    if user_exists:
        if password != user_exists["password"]:
            return """
                <h1>Password Incorrect!</h1>
                """

        session["USERNAME"] = user_exists["username"]

        return redirect(url_for("get_all_terms",
                                username=user_exists["username"]))
    else:
        return """
        <h1>User not found - try register instead</h1>
        """

# User register:
@app.route("/user_register")
def user_register():
    return render_template("user_register.html")

# checks the register credentials and loads the profile page:
@app.route("/save_new_user", methods=["POST"])
def save_new_user():
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]
    user_exists = users.find_one({"email": email})

    session["USERNAME"] = username

    if user_exists:
        return """
            <h1>User already exists - try logging in.</h1>
            """
    if len(username) < 4:
        return """
            <h1>Username too short.</h1>
            """
    if len(password) < 4:
        return """
            <h1>Password too short</h1>
            """

    users.insert_one(request.form.to_dict())

    # Create a field of type array to store term_ids
    users.update_one({"username": username},
                     {"$push": {"liked": ""}})

    return redirect(url_for("get_all_terms", username=username))

# Shows all of the user's terms
@app.route("/my_terms/<username>")
def my_terms(username):
    username = check_session_user(session)
    user = users.find_one({"username": username})

    return render_template("my_terms.html", user=user,
                           username=username,
                           terms=terms.find({"author": username}),
                           saved_terms=saved.find({"saved_by": username}))

# Show all terms in the database:
@app.route("/all_terms")
def get_all_terms():
    username = check_session_user(session)
    user = users.find_one({"username": username})

    # A way to display the number of times a term has been liked without having direct access to the term_id
    all_users = users.find()
    all_saved_ids = []
    for item in all_users:
        for num in item["liked"]:
            all_saved_ids.append(num)

    return render_template("all_terms.html",
                           username=username, user=user,
                           terms=terms.find(),
                           all_saved_ids=all_saved_ids,
                           saved_terms=saved.find({"saved_by": username}))

# When a term is clicked:
@app.route("/term/<term_id>")
def show_term(term_id):
    username = check_session_user(session)
    user = users.find_one({"username": username})

    term = terms.find_one({"_id": term_id})

    # use these variables to make a search unique (to the best degree possible)
    term_name = term["term"]
    term_definition = term["term_definition"]
    noob_definition = term["noob_definition"]
    term_examples = term["term_examples"]
    category_name = term["category_name"]
    # and check whether the term is in saved terms.
    is_in_database = saved.find_one({"saved_by": username,
                                     "term": term_name,
                                     "term_definition": term_definition,
                                     "noob_definition": noob_definition,
                                     "term_examples": term_examples,
                                     "category_name": category_name})

    already_liked = liked(term_id, user)
    number_of_likes = num_of_likes(term_id, users)

    return render_template("term.html", term=term,
                           is_in_database=is_in_database,
                           already_liked=already_liked,
                           number_of_likes=number_of_likes,
                           username=username, user=user,
                           saved_terms=saved.find({"saved_by": username}))

# Adds term_id to user's liked field
@app.route("/like/<term_id>")
def like(term_id):
    username = check_session_user(session)

    term = terms.find_one({"_id": term_id})

    users.update_one({"username": username},
                     {"$push": {"liked": term_id}})

    return redirect(url_for("show_term", term_id=term["_id"],
                            username=username))

# Removes term_id from user's liked field
@app.route("/unlike/<term_id>")
def unlike(term_id):
    username = check_session_user(session)

    term = terms.find_one({"_id": term_id})

    users.update_one({"username": username},
                     {"$pull": {"liked": term_id}})

    return redirect(url_for("show_term", term_id=term["_id"],
                            username=username))

# Add a new term (overwrites default ObjectId):
@app.route("/new_term")
def new_term():
    username = check_session_user(session)
    user = users.find_one({"username": username})

    random_string = uuid.uuid4().hex

    return render_template("new_term.html",
                           categories=categories.find({"author": username}),
                           new_id=random_string, user=user,
                           username=username,
                           saved_terms=saved.find({"saved_by": username}))

# Save the term to the database:
@app.route("/add_term", methods=["POST"])
def add_term():
    username = check_session_user(session)

    terms.insert_one(request.form.to_dict())

    return redirect(url_for("my_terms", username=username))

# Edit a term:
@app.route("/edit_term/<term_id>")
def edit_term(term_id):
    username = check_session_user(session)
    user = users.find_one({"username": username})

    term = terms.find_one({"_id": term_id})

    return render_template("edit_term.html", term=term,
                           categories=categories.find({"author": username}),
                           username=username, user=user,
                           saved_terms=saved.find({"saved_by": username}))

# Save your changes to the database once done editing:
@app.route("/save_term/<term_id>", methods=["POST"])
def save_term(term_id):
    username = check_session_user(session)

    the_term = terms.find_one({"_id": term_id})

    # check if term is in saved, then save changes there also
    saved_terms = saved
    # this search is as accurate as can be without having the id.
    # It matches each field exactly; the chance of 2 terms being identical to the letter is rare.
    in_saved = saved.find_one({"term": the_term["term"],
                               "category_name": the_term["category_name"],
                               "term_definition": the_term["term_definition"],
                               "noob_definition": the_term["noob_definition"],
                               "term_examples": the_term["term_examples"],
                               "author": the_term["author"]
                               })
    if in_saved:
        saved_terms.update_many(
            {"term": the_term["term"],
             "category_name": the_term["category_name"],
             "term_definition": the_term["term_definition"],
             "noob_definition": the_term["noob_definition"],
             "term_examples": the_term["term_examples"],
             "author": the_term["author"]},

            {"$set": {
             "term": request.form.get("term"),
             "category_name": request.form.get("category_name"),
             "term_definition": request.form.get("term_definition"),
             "noob_definition": request.form.get("noob_definition"),
             "term_examples": request.form.get("term_examples"),
             "author": request.form.get("author")}}, True)

    # saves the original term
    my_terms = terms
    my_terms.replace_one(
        {"_id": term_id}, {
         "term": request.form.get("term"),
         "category_name": request.form.get("category_name"),
         "term_definition": request.form.get("term_definition"),
         "noob_definition": request.form.get("noob_definition"),
         "term_examples": request.form.get("term_examples"),
         "author": request.form.get("author"),
         "saved_by": request.form.get("saved_by")
         })

    return redirect(url_for("my_terms", username=username))

# Delete a term request:
@app.route("/delete_request/<term_id>")
def delete_request(term_id):
    username = check_session_user(session)
    user = users.find_one({"username": username})

    term = terms.find_one({"_id": term_id})

    return render_template("delete_request.html",
                           term=term, user=user,
                           saved_terms=saved.find({"saved_by": username}))

# Shows chosen term and asks for confirmation before deleting:
@app.route("/delete_term/<term_id>")
def delete_term(term_id):
    username = check_session_user(session)

    terms.delete_one({"_id": term_id})

    return redirect(url_for("my_terms", username=username))

# Find a term in all terms:
@app.route("/find_term", methods=["POST"])
def find_term():
    username = check_session_user(session)
    user = users.find_one({"username": username})

    term_searched = request.form["term_search"]
    the_term = terms.find_one({"term": term_searched})

    if the_term:
        return redirect(url_for("show_term",
                                username=username,
                                term_id=the_term["_id"],
                                user=user))
    else:
        return """
            <h1>Oops! It seems your search was unsuccessful!</h1>
        """

# Show all categories:
@app.route("/categories")
def get_categories():
    username = check_session_user(session)
    user = users.find_one({"username": username})

    return render_template("categories.html",
                           categories=categories.find({"author": username}),
                           username=username, user=user,
                           saved_terms=saved.find({"saved_by": username}))

# When a category is clicked:
@app.route("/show_category/<category_id>")
def show_category(category_id):
    username = check_session_user(session)
    user = users.find_one({"username": username})

    category = categories.find_one({"_id": ObjectId(category_id)})

    return render_template("show_category.html",
                           username=username,
                           category=category, user=user,
                           saved_terms=saved.find({"saved_by": username}))

# Delete a category request:
@app.route("/delete_category_request/<category_id>")
def delete_category_request(category_id):
    username = check_session_user(session)
    user = users.find_one({"username": username})

    category = categories.find_one({"_id": ObjectId(category_id)})

    return render_template("delete_category_request.html",
                           username=username,
                           category=category, user=user,
                           saved_terms=saved.find({"saved_by": username}))

# Shows chosen category and asks for confirmation before deleting:
@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    categories.delete_one({"_id": ObjectId(category_id)})

    return redirect(url_for("get_categories"))

# Add a new category:
@app.route("/add_category")
def add_category():
    username = check_session_user(session)
    user = users.find_one({"username": username})

    return render_template("add_category.html",
                           username=username, user=user,
                           saved_terms=saved.find({"saved_by": username}))

# Save the new category to the database:
@app.route("/save_category", methods=["POST"])
def save_category():
    username = check_session_user(session)

    added_category = request.form["category_name"]
    is_in_database = categories.find_one({"category_name": added_category,
                                         "author": username})

    if is_in_database:
        return """
            <h1>Category already exists!</h1>
            """
    else:
        categories.insert_one(request.form.to_dict())
        return redirect(url_for("new_term"))

# Find a category:
@app.route("/find_category", methods=["POST"])
def find_category():
    username = check_session_user(session)
    user = users.find_one({"username": username})

    category_searched = request.form["category_search"]
    the_category = categories.find_one({"category_name": category_searched,
                                        "author": username})

    if the_category:
        return render_template("show_category.html",
                               category=the_category, user=user,
                               saved_terms=saved.find({"saved_by": username}))
    else:
        return """
            <h1>Oops! It seems your search was unsuccessful!</h1>
        """

# Shows the list of saved terms (Further Readings):
@app.route("/saved_terms")
def saved_terms():
    username = check_session_user(session)
    user = users.find_one({"username": username})

    return render_template("further_readings.html",
                           terms=saved.find({"saved_by": username}),
                           user=user, username=username,
                           saved_terms=saved.find({"saved_by": username}))

# When a further_readings term is clicked:
@app.route("/saved_term/<term_id>")
def show_saved_term(term_id):
    username = check_session_user(session)
    user = users.find_one({"username": username})

    term = saved.find_one({"_id": term_id})

    return render_template("saved_term.html", term=term,
                           username=username, user=user,
                           saved_terms=saved.find({"saved_by": username}))

# clones the term, changes the id, and populates saved_by to generate further readings list:
@app.route("/add_to_saved/<term_id>")
def add_to_saved(term_id):
    username = check_session_user(session)

    term = terms.find_one({"_id": term_id})

    # Finds which id the user clicked on and clones it.
    in_all_terms = terms.find_one({"_id": term_id})
    in_saved_terms = saved.find_one({"_id": term_id})

    if in_all_terms:
        the_term = terms.find({"_id": term_id})
    elif in_saved_terms:
        the_term = saved.find({"_id": term_id})

    cloned_term = the_term.clone()

    for doc in cloned_term:
        random_string = uuid.uuid4().hex
        doc["_id"] = random_string
        doc["saved_by"] = username
        saved.insert_one(doc)

        # Delay the redirect to give the JS toast time to escape before the page reloads
        time.sleep(1)

        return redirect(url_for("show_term", term_id=term["_id"]))


# Removes a document from the further_readings database:
@app.route("/remove_from_saved/<term_id>")
def remove_from_saved(term_id):
    username = check_session_user(session)
    user = users.find_one({"username": username})

    saved.delete_one({"_id": term_id})

    return redirect(url_for("saved_terms", username=username,
                            user=user))

# Find a saved term in further readings:
@app.route("/find_saved", methods=["POST"])
def find_saved():
    username = check_session_user(session)
    user = users.find_one({"username": username})

    term_searched = request.form["saved_search"]
    the_term = saved.find_one({"term": term_searched,
                              "saved_by": username})

    if the_term:
        return render_template("saved_term.html",
                               term=the_term, user=user,
                               saved_terms=saved.find({"saved_by": username}))
    else:
        return """
            <h1>Oops! It seems your search was unsuccessful!</h1>
        """


if __name__ == "__main__":
    app.run(host=os.environ.get("IP", "127.0.0.1"),
            port=os.environ.get("PORT", "5000"),
            debug=True)
