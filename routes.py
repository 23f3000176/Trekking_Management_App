from flask import Blueprint, flash, render_template, request

from models import User

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("home.html")

@main.route("/login")
def login():
    return render_template("login.html")

@main.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("Invalid username or password")
        return render_template("login.html")
    if not user.check_password(password):
        flash("Invalid username or password")
        return render_template("login.html")
    # Login successful
    return render_template("home.html")

@main.route("/register")
def register():
    return render_template("register.html")

@main.route("/register", methods=["POST"])
def register_post():
    username = request.form.get("username")
    password = request.form.get("password")
    name = request.form.get("name")
    role = request.form.get("role")
    if User.query.filter_by(username=username).first():
        flash("Username already exists")
        return render_template("register.html")
    user=User(username=username, password=password, name=name, role=role)
    db.session.add(user)
    db.session.commit()
    flash("Registration successful. Please log in.")
    return render_template("login.html")