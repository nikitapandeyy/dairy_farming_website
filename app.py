from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

# Function to create a new database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="dairy_farming"
    )

@app.route('/')
def home():
    return render_template('home.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            # Debug: print received username and password
            print("Received Username:", username)
            print("Received Password:", password)
            
            # Connect to the database
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            
            # Execute the query
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()
            
            # Debug: print fetched user
            print("Fetched User:", user)

            # Close the connection
            cursor.close()
            db.close()
            
            if user and check_password_hash(user['password'], password):
                session['username'] = user['username']
                session['role'] = user['role']
                # Debug: print session data
                print("Session Data:", session)
                if user['role'] == 'user':
                    return redirect(url_for('user_dashboard'))
                else:
                    return redirect(url_for('provider_dashboard'))
            else:
                flash("Invalid credentials. Please try again.", "danger")
                # Debug: flash message for invalid login
                print("Invalid credentials for user:", username)

        return render_template('login.html')
    except Exception as e:
        print("Error occurred:", e)
        flash("An error occurred during login. Please try again.", "danger")
        return render_template('login.html')

# User Dashboard
@app.route('/user_dashboard')
def user_dashboard():
    if 'username' in session and session['role'] == 'user':
        return render_template('user_dashboard.html')  # Make sure to render the template here
    flash("You need to log in as a user to access the user dashboard.", "warning")
    return redirect(url_for('login'))

# Provider Dashboard
@app.route('/provider_dashboard')
def provider_dashboard():
    if 'username' in session and session['role'] == 'provider':
        return render_template('provider_dashboard.html')  # Make sure to render the template here
    flash("You need to log in as a provider to access the provider dashboard.", "warning")
    return redirect(url_for('login'))

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change the port number if necessary

