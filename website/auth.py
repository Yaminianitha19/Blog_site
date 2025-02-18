from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_required, login_user,logout_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/login",methods=["GET", "POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    return render_template("login.html")

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists= User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash("Email already exists", category="error")
        elif username_exists:
            flash("Username already exists", category="error")
        elif password1 != password2:
            flash("Passwords don't match", category="error")
        elif len(username) < 2:
            flash("Username is too short", category="error")
        elif len(password1) < 6:
            flash("Password is too short", category="error")
        elif len(email) < 10:
            flash("Email in invalid", category="error")
        else:
            new_user = User(email=email, username=username, password=password1)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))







    return render_template("signup.html")

@auth.route("/logout")
def logout():
    return redirect(url_for("views.home"))
