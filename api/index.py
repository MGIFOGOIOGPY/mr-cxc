from flask import Flask, render_template_string, request, redirect, url_for, abort, make_response
import requests
from telegram import Bot
import ipinfo
from threading import Thread
import os
from collections import OrderedDict

app = Flask(__name__)

# ========== Configuration ==========
TELEGRAM_BOT_TOKEN = '7502616150:AAG-biBErcrZmHsrJ0JH-j83jNoaBtkvnKk'
TELEGRAM_ADMIN_ID = '7627713755'
IPINFO_TOKEN = 'YOUR_IPINFO_TOKEN'  # Get from ipinfo.io

# Initialize services
bot = Bot(token=TELEGRAM_BOT_TOKEN)
ip_handler = ipinfo.getHandler(IPINFO_TOKEN)

# User database with OrderedDict for potential scaling
users = OrderedDict({
    'admin': {'password': 'password123', 'max_users': 100}
})
max_total_users = 100

# ========== HTML Templates ==========
BASE_STYLE = """
<style>
    body { 
        background-color: #000; 
        color: #fff; 
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
    }
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    .btn {
        padding: 10px 15px;
        border: 1px solid #333;
        border-radius: 5px;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
    }
    .btn-black {
        background-color: #000;
        color: #fff;
    }
    .btn-black:hover {
        background-color: #222;
    }
    .text-error {
        color: #ff4444;
    }
    .text-success {
        color: #44ff44;
    }
</style>
"""

LOGIN_TEMPLATE = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Khalifa Souda</title>
    {BASE_STYLE}
    <style>
        .login-wrapper {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        .login-box {{
            background-color: #111;
            padding: 40px;
            border-radius: 10px;
            width: 350px;
            text-align: center;
        }}
        .login-logo {{
            width: 100px;
            height: 100px;
            border-radius: 50%;
            object-fit: cover;
            margin-bottom: 20px;
            border: 3px solid #333;
        }}
        .form-group {{
            margin-bottom: 20px;
            text-align: left;
        }}
        .form-control {{
            width: 100%;
            padding: 10px;
            background-color: #222;
            border: 1px solid #333;
            color: #fff;
            box-sizing: border-box;
        }}
    </style>
</head>
<body>
    <div class="login-wrapper">
        <div class="login-box">
            <img src="https://via.placeholder.com/100" alt="Logo" class="login-logo">
            <h2>Khalifa Souda</h2>
            
            {% if error %}
            <div class="text-error">{{ error }}</div>
            {% endif %}
            
            <form method="POST" action="/login">
                <div class="form-group">
                    <input type="text" name="username" class="form-control" placeholder="Username" required>
                </div>
                <div class="form-group">
                    <input type="password" name="password" class="form-control" placeholder="Password" required>
                </div>
                <button type="submit" class="btn btn-black">Login</button>
            </form>
        </div>
    </div>
</body>
</html>
"""

DASHBOARD_TEMPLATE = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    {BASE_STYLE}
    <style>
        .header {{
            background-color: #111;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #333;
        }}
        .logo {{
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid #333;
        }}
        .nav {{
            display: flex;
            background-color: #111;
            padding: 10px 0;
        }}
        .nav-item {{
            padding: 10px 20px;
            cursor: pointer;
        }}
        .content-card {{
            background-color: #111;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <img src="https://via.placeholder.com/60" alt="Logo" class="logo">
            <h2>Khalifa Souda</h2>
        </div>
        <a href="/logout" class="btn btn-black">Logout</a>
    </div>
    
    <div class="nav">
        <div class="nav-item">Religious Rulings</div>
        <div class="nav-item">Friday Sermon</div>
    </div>
    
    <div class="container">
        <div class="content-card">
            <h3>Welcome to the Dashboard</h3>
            <p>This is your secure area.</p>
        </div>
    </div>
</body>
</html>
"""

# ========== Helper Functions ==========
def send_telegram_alert(message):
    try:
        bot.send_message(chat_id=TELEGRAM_ADMIN_ID, text=message)
    except Exception as e:
        print(f"Telegram error: {str(e)}")

def get_ip_details(ip):
    try:
        details = ip_handler.getDetails(ip)
        return {
            'ip': ip,
            'city': details.city,
            'country': details.country_name,
            'org': details.org
        }
    except Exception as e:
        print(f"IP info error: {str(e)}")
        return {'ip': ip}

# ========== Routes ==========
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username]['password'] == password:
            ip = request.remote_addr
            ip_info = get_ip_details(ip)
            
            # Send login notification
            msg = f"✅ Successful login\nUser: {username}\nIP: {ip}\n"
            msg += f"Location: {ip_info.get('city', 'N/A')}, {ip_info.get('country', 'N/A')}"
            Thread(target=send_telegram_alert, args=(msg,)).start()
            
            response = make_response(redirect(url_for('dashboard')))
            response.set_cookie('auth_token', 'verified', max_age=3600)
            return response
        else:
            ip = request.remote_addr
            msg = f"⚠️ Failed login\nAttempt: {username}\nIP: {ip}"
            Thread(target=send_telegram_alert, args=(msg,)).start()
            return render_template_string(LOGIN_TEMPLATE, error="Invalid credentials")
    
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/dashboard')
def dashboard():
    if not request.cookies.get('auth_token'):
        return redirect(url_for('login'))
    return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.set_cookie('auth_token', '', expires=0)
    return response

# ========== Main Execution ==========
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
