from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Use the absolute path of the current directory to store 'users.json' inside the project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the current directory of app.py
USERS_FILE = os.path.join(BASE_DIR, 'users.json')  # Join the current directory with 'users.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        return []  # If the file doesn't exist, return an empty list
    with open(USERS_FILE, 'r') as f:
        try:
            data = json.load(f)
            if isinstance(data, list):  # Ensure the data is a list
                return data
            else:
                return []  # Return an empty list if data is not a list
        except json.JSONDecodeError:
            return []  # Return an empty list if the file is empty or contains invalid JSON

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/')
def index():
    return render_template('login_signup.html')

@app.route('/submit', methods=['POST'])
def submit():
    action = request.form.get('action')
    email = request.form.get('email')
    password = request.form.get('password')

    # Load users from the file (ensure it's a list)
    users = load_users()

    if action == 'signup':
        # Signup logic
        for user in users:
            if isinstance(user, dict) and user.get('email') == email:
                return "User already exists. Please login."
        users.append({'email': email, 'password': password})  # Append user as a dictionary
        save_users(users)  # Save updated users back to the file
        return redirect(url_for('home'))  # Redirect to home after successful signup

    elif action == 'login':
        # Login logic
        for user in users:
            if isinstance(user, dict) and user.get('email') == email and user.get('password') == password:
                return redirect(url_for('home'))  # Redirect to home if login is successful
        return "Invalid email or password."  # Return error message if login fails

    return "Invalid action."  # Return error message if action is invalid

@app.route('/home')
def home():
    return render_template('home.html')  # Render home page after successful login/signup

if __name__ == '__main__':
    app.run(debug=True)
