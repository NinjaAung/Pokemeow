from pynput.keyboard import Key, Controller
from selenium import webdriver
from dotenv import dotenv_values
from datetime import datetime
from time import sleep
import csv
import re


keyboard = Controller()
config = dotenv_values(".env")

members                 = []
members_join_date       = []
members_contribution    = []

driver = webdriver.Chrome("./drivers/chromedriver")

# Random Corp Server
# driver.get("https://discord.com/channels/719694038088810506/797292197811585066")

# Testing
driver.get("https://discord.com/channels/750761968067018859/797230922393976866")

username = config["USER_NAME"]
password = config["USER_PASSWORD"]
start_message = "Starting Count!"
pokemeow = ";clan members"
pokemeow_next = "next"
pruning = "t@prune 5"

def sanitazing(members,contrib):
    for i in range(0,len(members)):
        members[i]  = members[i][3:].strip()
        contrib[i]  = re.sub(r"\|.*","",contrib[i]).strip()


sleep(2)

for letter in username:
    keyboard.press(letter)
    keyboard.release(letter)

keyboard.press(Key.enter)
keyboard.release(Key.enter)

sleep(1)

for letter in password:
    keyboard.press(letter)
    keyboard.release(letter)

sleep(1)

keyboard.press(Key.enter)
keyboard.release(Key.enter)

sleep(6)
for letter in start_message:
    keyboard.press(letter)
    keyboard.release(letter)

keyboard.press(Key.enter)
keyboard.release(Key.enter)

sleep(1)

for letter in pokemeow:
    keyboard.press(letter)
    keyboard.release(letter)

keyboard.press(Key.enter)
keyboard.release(Key.enter)

sleep(2)

for i in range(0,4):
    sleep(2)
    try:
        member          = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/main/div[1]/div/div/div/div[5]/div[2]/div/div/div[4]/div[1]/div[2]").text.splitlines()
        contribution    = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/main/div[1]/div/div/div/div[5]/div[2]/div/div/div[4]/div[2]/div[2]").text.splitlines()
        date_joined     = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/main/div[1]/div/div/div/div[5]/div[2]/div/div/div[4]/div[3]/div[2]").text.splitlines()
    except:
        member          = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/main/div[1]/div/div/div/div[4]/div[2]/div/div/div[4]/div[1]/div[2]").text.splitlines()
        contribution    = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/main/div[1]/div/div/div/div[4]/div[2]/div/div/div[4]/div[2]/div[2]").text.splitlines()
        date_joined     = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/main/div[1]/div/div/div/div[4]/div[2]/div/div/div[4]/div[3]/div[2]").text.splitlines()
        
    sanitazing(member,contribution)
    members                 += member
    members_join_date       += date_joined 
    members_contribution    += contribution



    for letter in pokemeow_next:
        keyboard.press(letter)
        keyboard.release(letter)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

for letter in pruning:
    keyboard.press(letter)
    keyboard.release(letter)

keyboard.press(Key.enter)
keyboard.release(Key.enter)

Catch_Min=800
with open('RandomCorp_Catches.csv', "a", newline='') as f:
    fieldnames = ["Member","Today's Catch","Days Joined","Average Catch Rate"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(0,len(members)):
        timedelta = datetime.now() - datetime.fromisoformat(members_join_date[i])
        if timedelta.days <= 0:
            avg  = 0
            days = 0
            
        else:
            avg  = int(members_contribution[i].replace(",","")) / int(timedelta.days)
            days = timedelta.days

        writer.writerow({"Member":members[i],"Today's Catch":members_contribution[i].replace(",",""),"Days Joined":days,"Average Catch Rate":avg})




sleep(2)

driver.close()