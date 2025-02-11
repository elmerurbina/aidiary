# AI Diary - Final Exam for Database I

**AI Diary** is a web application designed as a personal diary assisted by artificial intelligence. It allows users to record and retrieve daily entries, interact with a chatbot, and manage their user profile. This project is part of the final exam for the **Database I** course.

---

## Description
AI Diary is a Flask-based web application that integrates a PostgreSQL database to store user data and diary entries. Users can interact with a chatbot to retrieve information from specific dates or add new entries. The application also includes a user profile management system where users can update their name, email, password, and profile photo.

---

## Functionalities
1. **User Registration and Authentication:**
   - Users can sign up and log in to access their personal diary.
   - Passwords are securely hashed before being stored in the database.

2. **Diary Entries:**
   - Users can write and save daily entries.
   - The chatbot allows users to retrieve entries from specific dates using commands like:
     ```
     quiero saber mis entradas del día yyyy-mm-dd
     ```

3. **Chatbot Interaction:**
   - The chatbot guides users to add new entries or retrieve old ones.
   - Provides dynamic responses based on user input.

4. **Profile Management:**
   - Users can update their profile information (name, email, password, and photo).
   - Passwords are only updated if a new one is provided; otherwise, the existing password is retained.

5. **Profile Photo:**
   - Users can upload a profile photo via a URL.
   - The photo is displayed in the navigation bar.

---

## Characteristics
- **User-Friendly Interface:** Simple and intuitive design for easy navigation.
- **Secure Authentication:** Passwords are hashed using `werkzeug.security`.
- **Dynamic Chatbot:** Provides interactive and helpful responses.
- **Database Integration:** Uses PostgreSQL for storing user data and diary entries.

---

## Technology Stack
- **Frontend:** HTML, CSS, JavaScript.
- **Backend:** Flask (Python).
- **Database:** PostgreSQL.
- **Authentication:** Flask sessions and password hashing.
- **Chatbot:** Custom logic implemented in Flask.

---

## How to Run the Application

### Prerequisites
1. **Python 3.x** installed.
2. **PostgreSQL** installed and running locally.
3. **Flask** and other dependencies installed.

### Steps to Run the App

1. **Set Up the Local Database:**
   - The file db_schema.sql contain the script for creating the DB, tables, Functions, Procedures

2. **Install Dependencies:**
   - Navigate to the project directory and install the required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

3. **Configure the Database Connection:**
   - update the .env file to match your credentials
   

4. **Run the Application:**
   - Execute the following command to start the Flask development server:
     ```bash
     python app.py
     ```
   - Open your browser and navigate to `http://127.0.0.1:5000` to access the application.

---

## Notes
- **No Migrations:** The database schema is simple, so no migration tools are used. The `users` table is created manually.
- **Flask Development Server:** The app is designed to run on Flask's built-in development server for simplicity.
- **Local Use Only:** This app is intended for local use as part of the **Database I** final exam.



 