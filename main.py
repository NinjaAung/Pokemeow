from pynput.keyboard import Key, Controller
from selenium import webdriver
from dotenv import dotenv_values
from time import sleep
import csv
import re

keyboard = Controller()
config = dotenv_values(".env")

driver = webdriver.Chrome("./drivers/chromedriver")
driver.get("https://discord.com/channels/719694038088810506/740628046284980390")

username = config["USER_NAME"]
password = config["USER_PASSWORD"]

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