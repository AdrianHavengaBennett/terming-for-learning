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

# Home screen / main welcome page:
@app.route("/")
def welcome():
    return render_template("home.html")

# Shows all the current terms in the database:
@app.route("/all_terms")
def get_terms():
    return render_template("all_terms.html", terms=terms.find())

# When a term is clicked:
@app.route("/term/<term_id>")
def show_term(term_id):
    term = terms.find_one({"_id": ObjectId(term_id)})
    return render_template("term.html", term=term,
                           further_readings=further_readings.find())

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
        return render_template("oops.html")  # TODO change this to a JS prompt to warn the user.
    else:
        categories.insert_one(request.form.to_dict())
    return redirect(url_for("get_categories"))


# Shows the list of saved terms (Further Readings):
@app.route("/saved_terms")
def saved_terms():
    return render_template("further_readings.html",
                           further_readings=further_readings.find())


# Copies a document and saves it to the further readings database:
@app.route("/add_to_saved/<term_id>")
def add_to_saved(term_id):
    term = terms.find_one({"_id": ObjectId(term_id)})
    further_readings.insert_one(term)
    return redirect(url_for("saved_terms"))


# Removes a document from the further readings database:
@app.route("/remove_from_saved/<term_id>")
def remove_from_saved(term_id):
    term = terms.find_one({"_id": ObjectId(term_id)})
    further_readings.remove(term)
    return redirect(url_for("saved_terms"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP", "5000"),
            port=os.environ.get("PORT", "5000"),
            debug=True)
