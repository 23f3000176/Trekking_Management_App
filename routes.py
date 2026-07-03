from flask import render_template, request, redirect, url_for, flash

from models import User, Trek, Booking

from app import app

@app.route("/")
def home():
    return render_template("home.html")