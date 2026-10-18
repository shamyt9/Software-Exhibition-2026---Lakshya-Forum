from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from database import users_col
from models import User
import bcrypt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET", "POST"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        # Find user in MongoDB
        user_data = users_col.find_one({"username": username, "is_active": True})

        if user_data and bcrypt.checkpw(password.encode(), user_data["password"]):
            user = User(user_data)
            login_user(user, remember=True)
            session.permanent = True

            # Log the login action
            from database import logs_col
            from datetime import datetime
            logs_col.insert_one({
                "user_id"     : str(user_data["_id"]),
                "action"      : "login",
                "details"     : f"{username} logged in",
                "action_at"   : datetime.utcnow()
            })

            flash(f"Welcome back, {user.full_name}!", "success")
            return redirect(url_for("dashboard.home"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    from database import logs_col
    from datetime import datetime
    logs_col.insert_one({
        "user_id"   : current_user.id,
        "action"    : "logout",
        "details"   : f"{current_user.username} logged out",
        "action_at" : datetime.utcnow()
    })
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))