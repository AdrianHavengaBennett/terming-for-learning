import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import pymongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["SECRET_KEY"] = "3ef;EFJH;DUGHA;dsjgn;IUDGS;ADJBV;DLSIUHGA;LSDJGHP;DUXH;UHNP;piouhpIUEHA;GU;RAWERAG;ODFIGH;AHG;AIOSUDG"

MONGODB_URI = os.getenv("MONGO_URI")
DBS_NAME = "terming_for_learning"
TERMS = "terms"
CATEGORIES = "categories"
FURTHER_READINGS = "further_readings"
USERS = "users"


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to Mongo: {}".format(e))


conn = mongo_connect(MONGODB_URI)
terms = conn[DBS_NAME][TERMS]
categories = conn[DBS_NAME][CATEGORIES]
further_readings = conn[DBS_NAME][FURTHER_READINGS]
users = conn[DBS_NAME][USERS]

# Home screen / main welcome page:
@app.route("/")
def welcome():
    return render_template("home.html")

# User login:
@app.route("/user_login")
def user_login():
    return render_template("user_login.html")

# checks the login credentials and loads the terms list:
@app.route("/valid_login", methods=["POST"])
def valid_login():
    email = request.form["email"]
    password = request.form["password"]
    user_exists = users.find_one({"email": email})
    # TODO more server-side validation
    if user_exists:
        if password != user_exists["password"]:
            return "Password Incorrect!"
        return redirect(url_for("get_terms", username=user_exists["username"]))
    else:
        return "User not found - try register instead"

# User register:
@app.route("/user_register")
def user_register():
    return render_template("user_register.html")

# checks the register credentials and loads the terms list:
@app.route("/save_new_user", methods=["POST"])
def save_new_user():
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]
    user_exists = users.find_one({"email": email})
    # TODO more server-side validation
    if user_exists:
        return "User already exists - try log in"
    if len(username) < 4:
        return "Username too short!"
    if len(password) < 4:
        return "Password too short!"
    users.insert_one(request.form.to_dict())
    return redirect(url_for("get_terms", username=username))

# Shows all the current terms in the database - this needs to change to user's terms only:
@app.route("/all_terms/<username>")
def get_terms(username):
    return render_template("all_terms.html", terms=terms.find(),
                           username=username)

# When a term is clicked:
@app.route("/term/<term_id>")
def show_term(term_id):
    term = terms.find_one({"_id": ObjectId(term_id)})
    active_user = term["username"]  # this needs to be session user, not user who added the term
    is_in_database = further_readings.find_one({"_id": ObjectId(term_id)})
    return render_template("term.html", term=term,
                           is_in_database=is_in_database,
                           username=active_user)

# Add a new term:
@app.route("/new_term")
def new_term():
    return render_template("new_term.html", categories=categories.find())

# Save the term to the database:
@app.route("/add_term", methods=["POST"])
def add_term():
    terms.insert_one(request.form.to_dict())
    return redirect(url_for("get_terms"))

# Edit a term:
@app.route("/edit_term/<term_id>")
def edit_term(term_id):
    term = terms.find_one({"_id": ObjectId(term_id)})
    all_categories = categories.find()
    return render_template("edit_term.html",
                           term=term, categories=all_categories)

# Save your changes to the database once done editing:
@app.route("/save_term/<term_id>", methods=["POST"])
def save_term(term_id):
    all_terms = terms
    all_terms.replace_one(
        {"_id": ObjectId(term_id)}, {
         "term": request.form.get("term"),
         "category_name": request.form.get("category_name"),
         "term_definition": request.form.get("term_definition"),
         "noob_definition": request.form.get("noob_definition"),
         "term_examples": request.form.get("term_examples"),
         "explore_more": request.form.get("explore_more")
         })
    return redirect(url_for("get_terms"))

# Delete a term:
@app.route("/delete_request/<term_id>")
def delete_request(term_id):
    term = terms.find_one({"_id": ObjectId(term_id)})
    return render_template("delete_request.html", term=term)

# Shows chosen term and asks for confirmation before deleting:
@app.route("/delete_term/<term_id>")
def delete_term(term_id):
    terms.delete_one({"_id": ObjectId(term_id)})
    return redirect(url_for("get_terms"))

# Show all categories:
@app.route("/categories")
def get_categories():
    return render_template("categories.html", categories=categories.find())

# When a category is clicked:
@app.route("/show_category/<category_id>")
def show_category(category_id):
    category = categories.find_one({"_id": ObjectId(category_id)})
    return render_template("show_category.html", category=category)

# Delete a category:
@app.route("/delete_category_request/<category_id>")
def delete_category_request(category_id):
    category = categories.find_one({"_id": ObjectId(category_id)})
    return render_template("delete_category_request.html", category=category)

# Shows chosen category and asks for confirmation before deleting:
@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    categories.remove({"_id": ObjectId(category_id)})
    return redirect(url_for("get_categories"))

# Add a new category:
@app.route("/add_category")
def add_category():
    return render_template("add_category.html", categories=categories.find())

# Save the new category to the database:
@app.route("/save_category", methods=["POST"])
def save_category():
    added_category = request.form["category_name"]  # This is what the user inputs
    is_in_database = categories.find_one({"category_name": added_category})  # This will need further validating (lowercase and uppercase, for example, and whitespace (there's a method that can do that - Google it))
    if is_in_database:
        return "Category already exists!"  # TODO change this to a JS prompt to warn the user.
    else:
        categories.insert_one(request.form.to_dict())
    return redirect(url_for("get_categories"))


# Shows the list of saved terms (Further Readings):
@app.route("/saved_terms")
def saved_terms():
    return render_template("further_readings.html",
                           further_readings=further_readings.find())


# Copies a document and saves it to the further_readings database:
@app.route("/add_to_saved/<term_id>")
def add_to_saved(term_id):
    term = terms.find_one({"_id": ObjectId(term_id)})
    further_readings.insert_one(term)
    return redirect(url_for("saved_terms"))


# Removes a document from the further_readings database:
@app.route("/remove_from_saved/<term_id>")
def remove_from_saved(term_id):
    term = terms.find_one({"_id": ObjectId(term_id)})
    further_readings.remove(term)
    return redirect(url_for("saved_terms"))

# Find a term:
@app.route("/find_term", methods=["POST"])
def find_term():
    # This requires some error checking and validation
    term_searched = request.form["term_search"]
    the_term = terms.find_one({"term": term_searched})
    if the_term:
        return render_template("term.html", term=the_term)
    else:
        return "Oops! It seems your search was unsuccessful!"  # TODO change this to a JS prompt to warn the user.

# Find a category:
@app.route("/find_category", methods=["POST"])
def find_category():
    # This requires some error checking and validation
    category_searched = request.form["category_search"]
    the_category = categories.find_one({"category_name": category_searched})
    if the_category:
        return render_template("show_category.html", category=the_category)
    else:
        return "Oops! It seems your search was unsuccessful!"  # TODO change this to a JS prompt to warn the user.

# Find a saved term in further readings:
@app.route("/find_saved", methods=["POST"])
def find_saved():
    # This requires some error checking and validation
    term_searched = request.form["saved_search"]
    the_term = terms.find_one({"term": term_searched})
    if the_term:
        return render_template("term.html", term=the_term)
    else:
        return "Oops! It seems your search was unsuccessful!"  # TODO change this to a JS prompt to warn the user.


if __name__ == "__main__":
    app.run(host=os.environ.get("IP", "127.0.0.1"),
            port=os.environ.get("PORT", "5000"),
            debug=True)
