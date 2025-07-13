from flask import Flask, request, redirect, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from db import conn

app = Flask(__name__, static_folder='public', static_url_path='')
CORS(app)

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return 'Missing username or password', 400

    hashed_password = generate_password_hash(password)

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        return redirect("http://localhost:3000/login.html")
    except Exception as e:
        return f"Signup failed: {str(e)}", 400

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and check_password_hash(user['password'], password):
        return 'Login successful!'
    else:
        return 'Invalid username or password.', 401

if __name__ == '__main__':
    app.run(port=5000, debug=True)
