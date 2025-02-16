import bcrypt
from flask import request, jsonify, session, render_template, redirect, url_for, flash
from models.models import User, DiaryEntry
from models.ai_model import handle_user_message

# Helper function to hash passwords using bcrypt
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()  # Store as string


# Helper function to verify passwords
def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

# Función para configurar todas las rutas
def setup_routes(app):
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
            password = request.form.get("password")

            # Retrieve the user
            user = User.get_user_by_email(email)
            if not user or not check_password(password, user[3]):  # user[3] is the hashed password
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
            password = request.form.get("password")
            photo = request.form.get("photo")

            # Hash the password before storing it
            hashed_password = hash_password(password)

            # Check if the user already exists
            if User.get_user_by_email(email):
                return render_template("signup.html", error="User already exists")

            # Create the user
            User.create_user(name, email, hashed_password, photo)
            return redirect(url_for("signin"))

        return render_template("signup.html")

    # Logout
    @app.route("/logout")
    def logout():
        session.clear()
        flash("Has cerrado sesión exitosamente.", "success")
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
    def profile():
        if "user_id" not in session:
            return jsonify({"error": "Unauthorized"}), 401

        user_id = session["user_id"]
        user = User.get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        return render_template("profile.html", user={
            "name": user[1],
            "email": user[2],
            "photo": user[4]
        })

    # Update Profile (With Concurrency Handling)
    @app.route("/update_profile", methods=["POST"])
    def update_profile():
        if "user_id" not in session:
            return redirect(url_for("signin"))

        user_id = session["user_id"]
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        photo = request.form.get("photo")

        # Hash the password only if it's provided
        hashed_password = hash_password(password) if password else None

        # Use a transaction to prevent race conditions
        try:
            User.update_user(user_id, name, email, hashed_password, photo)
            flash("Perfil Actualizado con exito!", "success")
        except Exception as e:
            flash("Error updating profile. Please try again.", "danger")

        return redirect(url_for("profile"))

    # Delete Profile (With Concurrency Handling)
    @app.route("/delete_profile", methods=["POST"])
    def delete_profile():
        if "user_id" not in session:
            return jsonify({"error": "Unauthorized"}), 401

        user_id = session["user_id"]

        # Use a transaction to ensure profile deletion is atomic
        try:
            User.delete_user(user_id)
            session.pop("user_id", None)  # Remove user from session
            return jsonify({"message": "Perfil eliminado exitosamente"})
        except Exception as e:
            return jsonify({"error": "Error deleting profile"}), 500

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
