from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

users = load_users()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    
    if not username or not email or not password:
        return "Missing fields", 400
    
    if username in users:
        return "Username already exists", 400
    
    users[username] = {"email": email, "password": password}
    save_users(users)
    return "Signup successful!"

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    for user, info in users.items():
        if info["email"] == email and info["password"] == password:
            return f"Welcome back, {user}!"
    
    return "Login failed! Incorrect email or password.", 400

if __name__ == "__main__":
    app.run(debug=True)
