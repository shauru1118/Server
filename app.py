from flask import Flask, send_from_directory, abort, render_template, url_for, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from telebot import TeleBot
import os
from random import randint

ALBERT = 5572914505

App = Flask(__name__)
App.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(App)

token = "7014079648:AAGMLeCdVqcnVydBA20OLnGyGu3Vkqi07Lk"
bot = TeleBot(token)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f'<User {self.id}>'


VIEWS_DIR = os.path.join(os.path.dirname(__file__), "templates")


@App.route("/")
@App.route("/home")
def index():
    return render_template("index.html")

@App.route("/app")
def app():
    return render_template("app.html")

@App.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_login = request.form.get("login")
        user_password = request.form.get("password")

        user = User.query.filter_by(login=user_login, password=user_password).first()
        
        if user:
            return f"Welcome, {user.name}!"
        else:
            try:
                db.session.add(User(name="Gost", login=user_login, password=user_password))
                db.session.commit()
                return redirect("/")
            except Exception as e:
                return f"Err:\n\n{e}"
            return "Invalid credentials. Please try again."
    else:
        return render_template("login.html")

@App.route("/account")
def account():
    return render_template("account.html")

@App.route("/not_found")
def not_found():
    return render_template("not_found.html"), 404

@App.route("/about")
def about():
    return render_template("about.html")

@App.route("/cases")
def case():
    return render_template("cases.html")

@App.route("/cases/<casename>")
def contact(casename):
    return render_template(f"{casename}.html")


@App.route("/<path:filename>")
def serve_page(filename):
    filepath = os.path.join(VIEWS_DIR, filename)
    if os.path.exists(filepath):
        return render_template(filename)
    else:
        return render_template("not_found.html"), 404




@App.route("/api/random_number")
def random_number():
    return str(randint(1, 100))


@App.route("/db")
@App.route("/download/db")
def download_db():
    bot.send_message(ALBERT, text="Download db")
    with open("instance/users.db", "rb") as file:
        bot.send_document(ALBERT, file)
    return redirect("/")




if __name__ == "__main__":
    print(VIEWS_DIR)
    port = int(os.environ.get("PORT", 8080))
    
    while True:
        App.run(host="0.0.0.0", port=port, debug=True)
        break
