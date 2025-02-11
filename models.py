import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection details
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# User Model
class User:
    @staticmethod
    def create_user(name, email, password, photo=None):
        """
        Calls the `insert_user` function in PostgreSQL to create a new user.
        """
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.callproc("insert_user", (name, email, password, photo))
            conn.commit()
        except psycopg2.Error as e:
            print(f"Error creating user: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def update_user(user_id, name=None, email=None, password=None, photo=None):
        """
        Calls the `update_user_profile` function in PostgreSQL to update a user's profile.
        """
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.callproc("update_user_profile", (user_id, name, email, password, photo))
            conn.commit()
        except psycopg2.Error as e:
            print(f"Error updating user: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def delete_user(user_id):
        """
        Calls the `delete_user_profile` function in PostgreSQL to delete a user.
        """
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.callproc("delete_user_profile", (user_id,))
            conn.commit()
        except psycopg2.Error as e:
            print(f"Error deleting user: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_user_by_email(email):
        """
        Calls the `get_user_by_email` function in PostgreSQL to retrieve a user by email.
        """
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.callproc("get_user_by_email", (email,))
            user = cur.fetchone()
            return user
        except psycopg2.Error as e:
            print(f"Error retrieving user: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_user_by_id(user_id):
        """
        Calls the `get_user_by_id` function in PostgreSQL to retrieve a user by ID.
        """
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.callproc("get_user_by_id", (user_id,))
            user = cur.fetchone()
            return user
        except psycopg2.Error as e:
            print(f"Error retrieving user: {e}")
            return None
        finally:
            cur.close()
            conn.close()

# Diary Entry Model
class DiaryEntry:
    @staticmethod
    def create_entry(user_id, entry_date, message):
        """
        Calls the `create_diary_entry` function in PostgreSQL to create a new diary entry.
        """
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.callproc("create_diary_entry", (user_id, entry_date, message))
            conn.commit()
        except psycopg2.Error as e:
            print(f"Error creating diary entry: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_entries_by_user(user_id):
        """
        Calls the `get_entries_by_user` function in PostgreSQL to retrieve all diary entries for a user.
        """
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.callproc("get_entries_by_user", (user_id,))
            entries = cur.fetchall()
            return entries
        except psycopg2.Error as e:
            print(f"Error retrieving diary entries: {e}")
            return []
        finally:
            cur.close()
            conn.close()