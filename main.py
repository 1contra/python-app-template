import os
import sys
import colorama
import platform
import requests
import keyboard as k
import customtkinter 
import tkinter as tk
from tkinter import *
from PIL import Image
from dhooks import Webhook
from urllib import response
from datetime import datetime
from tkinter import messagebox
from flask import Flask, request
from colorama import Back, Fore, Style
from CTkMessagebox import CTkMessagebox
from pynput.keyboard import Key, Listener 

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

        $$$$$$$\                   $$$$$$\                            $$$$$$$$\                                $$\            $$\               
        $$  __$$\                 $$  __$$\                           \__$$  __|                               $$ |           $$ |              
        $$ |  $$ |$$\   $$\       $$ /  $$ | $$$$$$\   $$$$$$\           $$ | $$$$$$\  $$$$$$\$$$$\   $$$$$$\  $$ | $$$$$$\ $$$$$$\    $$$$$$\  
        $$$$$$$  |$$ |  $$ |      $$$$$$$$ |$$  __$$\ $$  __$$\          $$ |$$  __$$\ $$  _$$  _$$\ $$  __$$\ $$ | \____$$\\_$$  _|  $$  __$$\ 
        $$  ____/ $$ |  $$ |      $$  __$$ |$$ /  $$ |$$ /  $$ |         $$ |$$$$$$$$ |$$ / $$ / $$ |$$ /  $$ |$$ | $$$$$$$ | $$ |    $$$$$$$$ |
        $$ |      $$ |  $$ |      $$ |  $$ |$$ |  $$ |$$ |  $$ |         $$ |$$   ____|$$ | $$ | $$ |$$ |  $$ |$$ |$$  __$$ | $$ |$$\ $$   ____|
        $$ |      \$$$$$$$ |      $$ |  $$ |$$$$$$$  |$$$$$$$  |         $$ |\$$$$$$$\ $$ | $$ | $$ |$$$$$$$  |$$ |\$$$$$$$ | \$$$$  |\$$$$$$$\ 
        \__|       \____$$ |      \__|  \__|$$  ____/ $$  ____/          \__| \_______|\__| \__| \__|$$  ____/ \__| \_______|  \____/  \_______|
                $$\   $$ |                $$ |      $$ |                                           $$ |                                       
                \$$$$$$  |                $$ |      $$ |                                           $$ |                                       
                 \______/                 \__|      \__|                                           \__|                                                                                                                                  
                                                                                                 
        {purple(f"__________________________________________________________________________________________________________")}
        {purple(f"[>] Python App Template 1.0.0")}
        {purple(f"[>] Running with Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}")}
"""
clear()
print(water(banner))

SERVER_URL = 'http://127.0.0.1:5000'
server = 'http://127.0.0.1:5000'

def login():

    root = customtkinter.CTk()
    root.geometry(f"{500}x{350}")
    root.title('Riot login')

    customtkinter.set_appearance_mode("dark")

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame, text="Riot Client")
    label.pack(pady=12, padx=10)

    username_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
    username_entry.pack(pady=12, padx=10)
    
    password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
    password_entry.pack(pady=12, padx=10)

    def submit_login():
        username = username_entry.get()
        password = password_entry.get()

    def onclick(event):
        username = username_entry.get()
        password = password_entry.get()
        data = {'username': username, 'password': password}
        response = requests.post(f'{SERVER_URL}/login', json=data)
        print(response.text)

        if response.status_code == 200:
            print(blue("Login successful"))
            print(purple("connected to" + ' ' + server))

            response.close()
            root.destroy()
                    
            class App(customtkinter.CTk):
                def __init__(self, *args, **kwargs,):
                    super().__init__(*args, **kwargs)
                    print(red("[^]ignore this[^]"))
              
                    self.title("Riot")
                    self.geometry(f"{1100}x{580}")

            if __name__ == "__main__":
                app = App()
                app.mainloop()
                
            
        elif response.status_code == 501:
            print(red("error 501 \nUser Was Banned"))
            msg = CTkMessagebox(title="Account Banned!", message="Account Banned!",
            icon="warning", option_1="retry")

        elif response.status_code == 601:
            print(red("error 601 \nUser Attempted to login more than once"))
            msg = CTkMessagebox(title="Already logged in!", message="Account already logged in!",
            icon="warning", option_1="retry")

        else:
            print(red("error 401 \nLogin Information Is Invalid"))
            msg = CTkMessagebox(title="Login Failure!", message="Login Info Invalid",
            icon="warning", option_1="retry")

    root.bind('<Return>', onclick)
    button = customtkinter.CTkButton(master=frame, text="Login", command = submit_login)
    button.bind('<Button-1>', onclick) 
    button.pack(pady=12, padx=10)

    if __name__ == "__main__":
        root.mainloop()
    
if __name__ == '__main__':
    login()








