from flask import Flask, send_from_directory, abort, render_template, url_for
import os
from time import sleep

App = Flask(__name__)

VIEWS_DIR = os.path.join(os.path.dirname(__file__), "templates")



@App.route("/")
@App.route("/home")
def index():
    return render_template("index.html")

@App.route("/app")
def app():
    return render_template("app.html")

@App.route("/not_found  ")
def not_found():
    return render_template("not_found.html"), 404

@App.route("/user/<username>/<id>")
def user(username, id):
    return f"<h1>Hello |{username}| with id |{id}| !</h1>"

@App.route("/<path:filename>")
def serve_page(filename):
    filepath = os.path.join(VIEWS_DIR, filename)
    if os.path.exists(filepath):
        return render_template(filename)
    else:
        return render_template("not_found.html"), 404

if __name__ == "__main__":
    print(VIEWS_DIR)
    port = int(os.environ.get("PORT", 8080))
    
    while True:
        App.run(host="0.0.0.0", port=port, debug=True)
