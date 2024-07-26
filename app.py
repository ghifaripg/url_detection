import requests
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import pandas as pd
import re
import tldextract
import pickle
from sklearn.feature_extraction import FeatureHasher
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import ssl
import socket

app = Flask(__name__)
app.secret_key = '1'  

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'csp'
}

# Load the trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Initialize the hasher
hasher = FeatureHasher(input_type='string', n_features=1024)

def extract_features(url):
    features = {}
    ext = tldextract.extract(url)
    features['domain'] = ext.domain
    features['subdomain'] = ext.subdomain
    features['suffix'] = ext.suffix
    features['has_ip'] = bool(re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', url))
    suspicious_tlds = ['top', 'info', 'xyzzy']
    features['suspicious_tld'] = ext.suffix in suspicious_tlds
    return features

def check_google_safe_browsing(api_key, url):
    api_url = 'https://safebrowsing.googleapis.com/v4/threatMatches:find?key=' + api_key
    data = {
        "client": {
            "clientId": "cspfinal",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }
    
    try:
        response = requests.post(api_url, json=data)
        response.raise_for_status()  # Raise an error for bad status codes

        if response.status_code == 200:
            result = response.json()
            if result.get('matches'):
                return True  # URL is unsafe
            else:
                return False  # URL is safe
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return False  # Assume URL is safe if there's an error

def check_ssl_certificate(url):
    try:
        hostname = url.split('//')[1].split('/')[0]
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                print(f"SSL certificate for {url} is valid.")
                return True
    except Exception as e:
        print(f"SSL certificate validation failed for {url}: {e}")
        return False

@app.route('/')
def home():
    username = session.get('username', None)
    return render_template('index.html', username=username)

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['newUsername']
    email = request.form['newEmail']
    password = request.form['newPass']
    confirm_password = request.form['confirmPass']

    # Check if passwords match
    if password != confirm_password:
        return '<script>alert("Passwords do not match"); window.location.href = "/login";</script>'

    # Connect to MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Hash the password
    hashed_password = generate_password_hash(password)

    try:
        cursor.execute("INSERT INTO users (Username, Email, Password) VALUES (%s, %s, %s)", (username, email, hashed_password))
        conn.commit()
        return '<script>alert("Registration Success"); window.location.href = "/login";</script>'
    except Exception as e:
        return f'<script>alert("Registration failed: {str(e)}"); window.location.href = "/login";</script>'
    finally:
        cursor.close()
        conn.close()

@app.route('/logining', methods=['POST'])
def login():
    username_or_email = request.form['username_or_email']
    password = request.form['password']

    # Connect to MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        # Check if username or email exists in database
        cursor.execute("SELECT * FROM users WHERE Username = %s OR Email = %s", (username_or_email, username_or_email))
        user = cursor.fetchone()

        if user:
            # Check if password matches the hashed password in database
            if check_password_hash(user[3], password):
                # Login successful, store username in session
                session['username'] = user[1]  # Assuming username is in the second column of users table
                return redirect(url_for('home'))
            else:
                return '<script>alert("Invalid password"); window.location.href = "/login";</script>'
        else:
            return '<script>alert("Username or email not found"); window.location.href = "/login";</script>'
    finally:
        cursor.close()
        conn.close()

@app.route('/account')
def account():
    # Check if user is logged in
    if 'username' not in session:
        return redirect(url_for('login_page'))

    # Connect to MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id, Username, Email, Created_at FROM users WHERE Username = %s", (session['username'],))
        user_info = cursor.fetchone()

        if user_info:
            cursor.execute("SELECT COUNT(*) AS total_searches FROM url_detections WHERE user_id = %s", (user_info['id'],))
            total_searches = cursor.fetchone()['total_searches']

            cursor.execute("SELECT COUNT(*) AS safe_count FROM url_detections WHERE user_id = %s AND detection_result = 'safe'", (user_info['id'],))
            safe_count = cursor.fetchone()['safe_count']

            cursor.execute("SELECT COUNT(*) AS malicious_count FROM url_detections WHERE user_id = %s AND detection_result = 'malicious'", (user_info['id'],))
            malicious_count = cursor.fetchone()['malicious_count']

            return render_template('account.html', user=user_info, total_searches=total_searches, safe_count=safe_count, malicious_count=malicious_count)
        else:
            return '<script>alert("User not found"); window.location.href = "/";</script>'
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return '<script>alert("An error occurred. Please try again later."); window.location.href = "/";</script>'
    finally:
        cursor.close()
        conn.close()

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    
    username = session['username']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id FROM users WHERE Username = %s", (username,))
        user_id = cursor.fetchone()['id']

        cursor.execute("SELECT url, detection_date, detection_result FROM url_detections WHERE user_id = %s ORDER BY detection_date DESC", (user_id,))
        detections = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    
    return render_template('history.html', detections=detections)

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form.get('url')
    features = extract_features(url)
    features_df = pd.DataFrame([features])
    
    # Hash the categorical features
    hashed_features = hasher.transform(features_df[['domain', 'subdomain', 'suffix']].astype(str).values)
    
    # Convert the sparse matrix to DataFrame directly without converting to dense
    hashed_df = pd.DataFrame.sparse.from_spmatrix(hashed_features, columns=[f'hash_{i}' for i in range(hashed_features.shape[1])])
    
    # Concatenate the hashed features with the original dataframe
    features_df = pd.concat([features_df.drop(columns=['domain', 'subdomain', 'suffix']), hashed_df], axis=1)
    
    # Check Google Safe Browsing API
    api_key = 'AIzaSyB68uOVxxc7g51PzbiDdTG4eD-cLOZQ-fM' 
    google_safe_browsing_result = check_google_safe_browsing(api_key, url)
    
    # Check SSL certificate validity
    ssl_check_result = check_ssl_certificate(url)
    
    # Predict with the local model
    prediction = model.predict(features_df)[0]
    result = 'safe' if prediction == 1 else 'malicious'
    
    # Override result based on external checks
    if google_safe_browsing_result or not ssl_check_result:
        result = 'malicious'
    
    if 'username' in session:
        username = session['username']
        
        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        try:
            # Get user ID
            cursor.execute("SELECT id FROM users WHERE Username = %s", (username,))
            user_id = cursor.fetchone()[0]

            # Save detection result to the database
            cursor.execute("INSERT INTO url_detections (user_id, url, detection_result) VALUES (%s, %s, %s)", (user_id, url, result))
            conn.commit()
        finally:
            cursor.close()
            conn.close()
    
    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True)
