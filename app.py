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
        print("Could not connect to Mongo: %s") % e


conn = mongo_connect(MONGODB_URI)
terms = conn[DBS_NAME][TERMS]
categories = conn[DBS_NAME][CATEGORIES]


@app.route("/")
def welcome():
    return render_template("home.html")


@app.route("/all_terms")
def get_terms():
    return render_template("all_terms.html", terms=terms.find())


@app.route("/term/<term_id>")
def show_term(term_id):
    term = terms.find_one({"_id": ObjectId(term_id)})
    return render_template("term.html", term=term)


@app.route("/categories")
def get_categories():
    return render_template("categories.html", categories=categories.find())


if __name__ == "__main__":
    app.run(host=os.environ.get("IP", "5000"),
            port=os.environ.get("PORT", "5000"),
            debug=True)
