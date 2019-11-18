import os
from flask import Flask

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "task_manager"
app.config["MONGO_URI"] = "mongodb+srv://InvAdrian:Iambutts1985@myfirstcluster-e8a5p.mongodb.net/terming_for_learning?retryWrites=true&w=majority"


@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(host=os.environ.get("IP", "5000"),
            port=os.environ.get("PORT", "5000"),
            debug=True)
