from pynput.keyboard import Key, Controller
from selenium import webdriver
from dotenv import dotenv_values
from time import sleep
import csv
import re

keyboard = Controller()
config = dotenv_values(".env")

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

sleep(5)
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
        members         = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/main/div[1]/div/div/div/div[5]/div[2]/div/div/div[4]/div[1]/div[2]").text
        contribution    = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/main/div[1]/div/div/div/div[5]/div[2]/div/div/div[4]/div[2]/div[2]").text
        date_joined     = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/main/div[1]/div/div/div/div[5]/div[2]/div/div/div[4]/div[3]/div[2]").text
    except:
        members         = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/main/div[1]/div/div/div/div[4]/div[2]/div/div/div[4]/div[1]/div[2]").text
        contribution    = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/main/div[1]/div/div/div/div[4]/div[2]/div/div/div[4]/div[2]/div[2]").text
        date_joined     = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/main/div[1]/div/div/div/div[4]/div[2]/div/div/div[4]/div[3]/div[2]").text
        
    print(date_joined)

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



