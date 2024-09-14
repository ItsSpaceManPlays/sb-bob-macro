from pynput import keyboard
from pynput.keyboard import Controller, Key
import pyautogui
import os
import time
import threading
import requests
import json
import discord
from datetime import datetime
from ahk import AHK
import argparse

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--no-alt-afk", action="store_true", help="Disable alt afk")

args = argument_parser.parse_args()

running = False
exit_flag = False

ahk = AHK()

if args.no_alt_afk:
    print("Alt afk disabled")

json_data = None
if not os.path.exists("settings.json"):
    with open('settings.json', "w") as f:
        json.dump({
            "webhook": "",
            "userId": 1
        }, f, indent=3)

    print("Please fill out proper data for settings.json")
    time.sleep(3)
    exit()
else:
    try:
        with open('settings.json', 'r') as f:
            json_data = json.load(f)
            usrid = json_data["userId"]
            wbhk = json_data["webhook"]

            name = requests.request('GET', f"https://users.roblox.com/v1/users/{usrid}").json()["name"]

            print(f"Found player: @{name} and connected to webhook {wbhk}")

    except Exception as e:
        print(e)
        time.sleep(3)
        exit()

if json_data["webhook"] == "" or json_data["userId"] < 2:
    print("Please fill out proper data for settings.json")
    time.sleep(3)
    exit()

if not args.no_alt_afk:
    print("Reading alt window position...")
    time.sleep(3)
    alt_position = pyautogui.position()
    print(f"Selected: {alt_position}")

webhook = json_data["webhook"]

def postToWebhook():
    if type(webhook) is not discord.SyncWebhook:
        webhook = discord.SyncWebhook.from_url(webhook)
    embed = discord.Embed(title="Bob has been obtained", description="Rob was obtained at: " + str(datetime.now().hour) + ":" + str(datetime.now().minute))
    webhook.send(embed=embed)

bobBadgeId = 2125950512

def checkBadge(userId):
    apiendpoint = "https://badges.roblox.com/v1/users/" + str(userId) + "/badges?sortOrder=Desc"
    try:
        respons = requests.get(apiendpoint)
        if respons.status_code != 200:
            return False
        
        jsonDecode = respons.json()
        for badge in jsonDecode["data"]:
            if badge["id"] == bobBadgeId:
                return True
            
        return False
    except:
        print("Internet connection lost, uh oh")
        

myKeyboard = Controller()

print("Press F6 to toggle, press F7 to close")
print("Started")

alt_antiafk_interval = 30
curr_count = 1

def anti_alt_afk():
    old_pos = pyautogui.position()

    pyautogui.moveTo(alt_position.x, alt_position.y)
    ahk.click()
    ahk.click()

    time.sleep(0.05)

    ahk.send('e')
    pyautogui.moveTo(old_pos.x, old_pos.y)
    ahk.click()
    ahk.click()
    
    time.sleep(0.05)

def presse():
    global running, exit_flag
    global curr_count
    while not exit_flag:
        if running:
            myKeyboard.press('e')
            myKeyboard.release('e')
            curr_count = (curr_count + 1) % (alt_antiafk_interval / 0.5)
            if curr_count == 0:
                if not args.no_alt_afk:
                    anti_alt_afk()

        time.sleep(0.5)

def checkBadgeCondition():
    global running, exit_flag
    while not exit_flag:
        if running:
            hasBadge = checkBadge(json_data["userId"])
            if hasBadge:
                print("done")
                postToWebhook()
                time.sleep(2)
                os._exit(0)
        time.sleep(6)

thread = threading.Thread(target=presse)
thread.start()
badgeThread = threading.Thread(target=checkBadgeCondition)
badgeThread.start()

def on_press(key):
    global running, exit_flag
    try:
        if key == Key.f6:
            running = not running
            os.system("title Running" if running else "title Not running")
        elif key == Key.f7:
            print("Stopping")
            running = False
            exit_flag = True
            listener.stop()
    except:
        pass

def on_release(key):
    pass

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

print("hi")
