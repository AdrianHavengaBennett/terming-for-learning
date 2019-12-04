import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import pymongo
from bson.objectid import ObjectId

app = Flask(__name__)

MONGODB_URI = os.getenv("MONGO_URI")
DBS_NAME = "terming_for_learning"
TERMS = "terms"
CATEGORIES = "categories"


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to Mongo: {}".format(e))


conn = mongo_connect(MONGODB_URI)
terms = conn[DBS_NAME][TERMS]
categories = conn[DBS_NAME][CATEGORIES]

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
    return render_template("term.html", term=term)

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
    all_terms.update({"_id": ObjectId(term_id)}, {
                      "term": request.form.get("term"),
                      "category_name": request.form.get("category_name"),
                      "term_definition": request.form.get("term_definition"),
                      "noob_definition": request.form.get("noob_definition"),
                      "term_examples": request.form.get("term_examples"),
                      "explore_more": request.form.get("explore_more")
                      })
    return redirect(url_for("get_terms"))


# Delete a term:
# At the moment, this will delete the term immediately. You'll need to edit it later so that it asks first.
@app.route("/delete_term/<term_id>")
def delete_term(term_id):
    terms.remove({"_id": ObjectId(term_id)})
    return redirect(url_for("get_terms"))

# Show all categories:
@app.route("/categories")
def get_categories():
    return render_template("categories.html", categories=categories.find())

# Add a new category:
@app.route("/add_category")
def add_category():
    return render_template("add_category.html")

# Save the new category to the database:
@app.route("/save_category", methods=["POST"])
def save_category():

    return redirect(url_for("get_categories"))
    pass


if __name__ == "__main__":
    app.run(host=os.environ.get("IP", "5000"),
            port=os.environ.get("PORT", "5000"),
            debug=True)
