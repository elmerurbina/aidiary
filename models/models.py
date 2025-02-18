import os
import psycopg2
from psycopg2 import pool
import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection details
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Initialize the connection pool
try:
    # Creating a connection pool with min and max connections
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        1,  # Min number of connections
        10, # Max number of connections
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    print("Connection pool created successfully")
except psycopg2.Error as e:
    print(f"Error creating connection pool: {e}")

# Database connection function using the pool
def get_db_connection():
    conn = connection_pool.getconn()  # Get a connection from the pool
    if conn is None:
        raise Exception("Unable to obtain a connection from the pool")
    return conn

# User Model
class User:

    db_table = "users"


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
            connection_pool.putconn(conn)  # Return the connection to the pool

    @staticmethod
    def generic_update_user(user_id, **kwargs):
        """
        Actualiza el perfil de usuario en la base de datos con los campos proporcionados.
        """
        conn = get_db_connection()
        cur = conn.cursor()

        fields = []

        for key, value in kwargs.items():
            if isinstance(value, str):
                value = f"'{value}'"
            fields.append(f"{key} = {value}")

        sql = f"UPDATE {User.db_table} SET {', '.join(fields)} WHERE id = {user_id}"

        try:
            cur.execute(sql)
            conn.commit()
        except psycopg2.Error as e:
            print(f"Error actualizando el perfil de usuario: {e}")
            conn.rollback()
        finally:
            cur.close()
            connection_pool.putconn(conn)


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
            connection_pool.putconn(conn)

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
            connection_pool.putconn(conn)

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
            connection_pool.putconn(conn)

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
            connection_pool.putconn(conn)

# Diary Entry Model
class DiaryEntry:
    @staticmethod
    def create_entry(user_id, message):
        """
        Calls the `create_diary_entry` function in PostgreSQL to create a new diary entry.
        """
        conn = get_db_connection()
        cur = conn.cursor()
        try:

            cur.callproc("create_diary_entry", (user_id, message))
            conn.commit()

        except psycopg2.Error as e:
            print(f"Error creating diary entry: {e}")
            conn.rollback()
        finally:
            cur.close()
            connection_pool.putconn(conn)

    @staticmethod
    def get_entries_by_user(user_id, entry_date):
        """
        Calls the `get_entries_by_user` function in PostgreSQL to retrieve all diary entries for a user on a specific date.
        """
        conn = get_db_connection()
        cur = conn.cursor()
        try:

            cur.callproc("get_entries_by_user", (user_id, entry_date))
            entries = cur.fetchall()

            return entries
        except psycopg2.Error as e:

            return []
        finally:
            cur.close()
            connection_pool.putconn(conn)
