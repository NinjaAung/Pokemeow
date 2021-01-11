from oauth2client.service_account   import ServiceAccountCredentials
from pynput.keyboard                import Key, Controller
from selenium                       import webdriver
from dotenv                         import dotenv_values
from datetime                       import datetime
from time                           import sleep
import gspread
import re

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
client = gspread.authorize(creds)

sheet = client.open_by_key("1hgHs8gCUOWnUsCBMw122XTSQeLCzRMa1C1FXT_OusnI").sheet1

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


new_member_cells_list       = sheet.range('H2:H51')
new_contribution_cells_list = sheet.range('I2:I51')
new_days                    = sheet.range('J2:J51')



#TODO: Record everything to gspread
for i in range(0,len(members)):
    timedelta = datetime.now() - datetime.fromisoformat(members_join_date[i])
    if timedelta.days <= 0:
        avg  = 0
        days = 0
        
    else:
        avg  = int(members_contribution[i].replace(",","")) / int(timedelta.days)
        days = timedelta.days

    new_member_cells_list[i].value          = members[i]
    new_contribution_cells_list[i].value    = members_contribution[i]
    new_days[i].value                       = days

#TODO: if user dosen't  exsist create a new row

sheet.update_cells(new_member_cells_list)
print("Members Added ✅")
sheet.update_cells(new_contribution_cells_list)
print("Contrinutions Added ✅")
sheet.update_cells(new_days)
print("Stay Added ✅")



sleep(2)

driver.close()