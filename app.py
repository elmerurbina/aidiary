import os
from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from models import User, DiaryEntry
import hashlib
from ai_model import handle_user_message

app = Flask(__name__)
app.secret_key = os.urandom(56)


# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Home Page
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("signin"))

    user_id = session["user_id"]
    user = User.get_user_by_id(user_id)
    if not user:
        return redirect(url_for("signin"))

    return render_template("home.html", user={
        "name": user[1],
        "email": user[2],
        "photo": user[4]
    })


# Sign-In Page
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = hash_password(request.form.get("password"))

        # Retrieve the user
        user = User.get_user_by_email(email)
        if not user or user[3] != password:  # user[3] is the password field
            return render_template("signin.html", error="Invalid email or password")

        # Store user ID in session
        session["user_id"] = user[0]  # user[0] is the user_id field
        return redirect(url_for("home"))

    return render_template("signin.html")


# Sign-Up Page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = hash_password(request.form.get("password"))
        photo = request.form.get("photo")

        # Check if the user already exists
        if User.get_user_by_email(email):
            return render_template("signup.html", error="User already exists")

        # Create the user
        User.create_user(name, email, password, photo)
        return redirect(url_for("signin"))

    return render_template("signup.html")


# Logout
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("signin"))


# Chat Endpoint
@app.route("/chat", methods=["POST"])
def chat():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    user_id = session["user_id"]
    message = data.get("message")

    response = handle_user_message(user_id, message)
    return jsonify({"response": response})


# Retrieve User Profile
@app.route("/profile", methods=["GET"])
def get_profile():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session["user_id"]
    user = User.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "user_id": user[0],
        "name": user[1],
        "email": user[2],
        "photo": user[4],
        "created_at": user[5],
        "updated_at": user[6]
    })


# Retrieve Diary Entries
@app.route("/entries", methods=["GET"])
def get_entries():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session["user_id"]
    entries = DiaryEntry.get_entries_by_user(user_id)
    if not entries:
        return jsonify({"error": "No entries found"}), 404

    return jsonify([{
        "entry_id": entry[0],
        "user_id": entry[1],
        "entry_date": entry[2],
        "message": entry[3],
        "created_at": entry[4],
        "updated_at": entry[5]
    } for entry in entries])


if __name__ == "__main__":
    app.run(debug=True)