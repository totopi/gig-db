from flask import Flask, render_template, jsonify, redirect
# from flask_pymongo import PyMongo
import os

app = Flask(__name__)
# app.config["MONGO_URI"] = os.environ['MONGODB_URI']
# mongo = PyMongo(app)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
