from flask import Flask, render_template, request, redirect, session
import sqlite3
import bcrypt

app = Flask(__name__)

# Secret key for sessions
app.secret_key = "secure-login-secret-key"


# Create database
def create_database():

    connection = sqlite3.connect("users.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# Home page
@app.route("/")
def home():

    if "username" in session:
        return redirect("/dashboard")

    return redirect("/login")


# Register
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if len(username) < 3:
            return "Username must contain at least 3 characters."

        if len(password) < 6:
            return "Password must contain at least 6 characters."

        # Hash password using bcrypt
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        try:

            connection = sqlite3.connect("users.db")

            cursor = connection.cursor()

            # Parameterized query protects against SQL injection
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password_hash.decode("utf-8"))
            )

            connection.commit()
            connection.close()

            return redirect("/login")

        except sqlite3.IntegrityError:

            return "Username already exists."

    return render_template("register.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = sqlite3.connect("users.db")

        cursor = connection.cursor()

        # Parameterized query
        cursor.execute(
            "SELECT username, password FROM users WHERE username = ?",
            (username,)
        )

        user = cursor.fetchone()

        connection.close()

        if user:

            stored_password = user[1]

            if bcrypt.checkpw(
                password.encode("utf-8"),
                stored_password.encode("utf-8")
            ):

                session["username"] = username

                return redirect("/dashboard")

        return "Invalid username or password."

    return render_template("login.html")


# Dashboard
@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


# Logout
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


if __name__ == "__main__":

    create_database()

    app.run(debug=True)