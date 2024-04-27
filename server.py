import os
import sys
import json
import base64
import colorama
import platform
import requests
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from functools import wraps
from urllib import response
from datetime import datetime
from cryptography.fernet import Fernet
from itertools import combinations
from colorama import Back, Fore, Style
from flask import Flask, request, Response, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

is_windows = True if platform.system() == "Windows" else False
colorama.init(autoreset=True)

def clear():
    if is_windows:
        os.system("cls")
    else:
        os.system("clear")

def pause():
    if is_windows:
        os.system(f"pause >nul")
    else:
        input()

def leave():
    try:
        sys.exit()
    except:
        exit()

def error(error):
    print(red(f"        [>] Error: {error}"), end="")
    pause(); clear(); leave()


def red(text):
    os.system(""); faded = ""
    for line in text.splitlines():
        green = 250
        for character in line:
            green -= 5
            if green < 0:
                green = 0
            faded += (f"\033[38;2;255;{green};0m{character}\033[0m")
        faded += "\n"
    return faded

def blue(text):
    os.system(""); faded = ""
    for line in text.splitlines():
        green = 0
        for character in line:
            green += 3
            if green > 255:
                green = 255
            faded += (f"\033[38;2;0;{green};255m{character}\033[0m")
        faded += "\n"
    return faded

def water(text):
    os.system(""); faded = ""
    green = 10
    for line in text.splitlines():
        faded += (f"\033[38;2;0;{green};255m{line}\033[0m\n")
        if not green == 255:
            green += 15
            if green > 255:
                green = 255
    return faded

def purple(text):
    os.system("")
    faded = ""
    down = False

    for line in text.splitlines():
        red = 40
        for character in line:
            if down:
                red -= 3
            else:
                red += 3
            if red > 254:
                red = 255
                down = True
            elif red < 1:
                red = 30
                down = False
            faded += (f"\033[38;2;{red};0;220m{character}\033[0m")
    return faded
banner = f"""
         ____       _       ____   _  __  _____   _   _   ____  
        | __ )     / \     / ___| | |/ / | ____| | \ | | |  _ \ 
        |  _ \    / _ \   | |     | ' /  |  _|   |  \| | | | | |
        | |_) |  / ___ \  | |___  | . \  | |___  | |\  | | |_| |
        |____/  /_/   \_\  \____| |_|\_\ |_____| |_| \_| |____/ 
                                                         
                                                                                                                               
                                     
        {purple(f"___________________________________________________")}
        {purple(f"[>] Python App Template Backend 1.0.0")}
        {purple(f"[>] Running with Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}")}

"""
clear()
print(water(banner))

app = Flask(__name__, template_folder='', static_folder='')
CORS(app)

WEBHOOK_URL = ""
SSL_CONTEXT = ('cert.pem', 'key.pem')

HOST = '127.0.0.1'
PORT =  6001

active_users = {

}

banned = {

}

ssl_cert = os.path.join(os.path.dirname(__file__), 'your_cert.pem')
ssl_key = os.path.join(os.path.dirname(__file__), 'your_key.pem')

options = {
    'bind': f'{HOST}:{PORT}',
    'keyfile': ssl_key,
    'certfile': ssl_cert
}

def load_user_data():
    try:
        with open('user_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_user_data(user_data):
    with open('user_data.json', 'w') as file:
        json.dump(user_data, file, indent=4)

def validate_credentials(username, password, user_data):
    if username in user_data:
        stored_password = user_data[username][0]
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_password == stored_password:
            return True
    return False

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


#if you want to link the logins or any event to a discord webhook, or just any webhook in general
def send_discord_notification(message):
    data = {"content": message}
    headers = {"Content-Type": "application/json"}
    response = requests.post(WEBHOOK_URL, json=data, headers=headers)
    if response.status_code != 204:
        print("Failed to send Discord notification")

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user_data = load_user_data()
    
    if username in active_users:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f" user `{username}` attempted to login more than once `{current_time}`"
        send_discord_notification(message)
        return 'User Attempted to login more than once.', 601

    if username in banned:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Banned user `{username}` has attempted to login but was denied access `{current_time}`"
        send_discord_notification(message)
        return 'user banned', 501

    if validate_credentials(username, password, user_data):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"`{username}` has logged in at `{current_time}`"
        send_discord_notification(message)
        ip_address = request.remote_addr
        print(blue(f"{username} Logged in from {ip_address}"))
        return 'Login successful', 200
        
    else:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message2 = f"`{username}` has failed to login `{current_time}`"
        send_discord_notification(message2)
        return 'Invalid credentials', 401
    
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    ip_address = request.remote_addr
    user_data = load_user_data()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if username in user_data:
        message1 = f" user attempted to signup using `{username}` but is already taken `{current_time}`"
        send_discord_notification(message1)
        return 'Username already exists. Please choose a different one.', 301
    
    hashed_password = hash_password(password)
    hashed_ip = hash_password(ip_address)
    user_data[username] = [hashed_password, hashed_ip]
    save_user_data(user_data)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"`{username}` has signed up at `{current_time}`"
    send_discord_notification(message)
    return 'Signup successful', 200

if __name__ == '__main__':
    import threading
    app.run(HOST, PORT, debug=True)