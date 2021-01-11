from oauth2client.service_account   import ServiceAccountCredentials
from pynput.keyboard                import Key, Controller
from selenium                       import webdriver
from dotenv                         import dotenv_values
from datetime                       import datetime
from time                           import sleep
import gspread
import re

# Google Creds
scope  = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/spreadsheets']
creds  = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1hgHs8gCUOWnUsCBMw122XTSQeLCzRMa1C1FXT_OusnI").sheet1

# Config
config   = dotenv_values(".env")
USERNAME = config["USER_NAME"]
PASSWORD = config["USER_PASSWORD"]

# Messages
start_message   = "Starting Count!"
pokemeow        = ";clan members"
pokemeow_next   = "next"
pruning         = "t@prune 5"

# Vaiables
curr_members              = []
curr_members_join_date    = []
curr_members_contribution = []

driver   = webdriver.Chrome("./drivers/chromedriver")
keyboard = Controller()
# driver.get("https://discord.com/channels/719694038088810506/797292197811585066") # Random Corp Server
driver.get("https://discord.com/channels/750761968067018859/797230922393976866") # Testing
keyboard = Controller()

def sanitazing(members,contrib):
    for i in range(0,len(members)):
        members[i]  = members[i][3:].strip()
        contrib[i]  = re.sub(r"\|.*","",contrib[i]).strip()

def typing(message,start_in=0,start_next=0):
    sleep(start_in)
    for letter in message:
        keyboard.press(letter)
        keyboard.release(letter)

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    sleep(start_next)


typing(USERNAME,2)
typing(PASSWORD,2)
typing(start_message,6)
typing(pokemeow,1)


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

    curr_members                 += member
    curr_members_join_date       += date_joined 
    curr_members_contribution    += contribution

    typing(1,pokemeow_next)

typing(1,2)

curr_member_cells_list       = sheet.range('H2:H51')
curr_contribution_cells_list = sheet.range('I2:I51')
curr_days                    = sheet.range('J2:J51')
past_members_list            = sheet.range('F2:F51')


for i in range(0,len(curr_members)):
    timedelta = datetime.now() - datetime.fromisoformat(curr_members_join_date[i])
    if curr_members[i] == "":
        curr_members[i] = ":fries:"
    if timedelta.days <= 0:
        days = 1
    else:
        days = timedelta.days

    curr_member_cells_list[i].value          = curr_members[i]
    curr_contribution_cells_list[i].value    = curr_members_contribution[i]
    curr_days[i].value                       = days


# sheet.update_cells(curr_member_cells_list)
# print("Members Added ✅")
# sheet.update_cells(curr_contribution_cells_list)
# print("Contributions Added ✅")
# sheet.update_cells(curr_days)
# print("Stay Added ✅")

#TODO: If a member leaves delete that row then format

for i in range(len(past_members_list)):
    if not past_members_list[i].value in curr_members:
        if past_members_list[i].value == "":
            break
        print(past_members_list[i].value)
        sheet.update_cell(past_members_list[i].row,1,"")
        sheet.update_cell(past_members_list[i].row,2,"")
        sheet.update_cell(past_members_list[i].row,3,"")
        sheet.update_cell(past_members_list[i].row,6,"1")

#TODO: IF a new member appears append to the list

for i in range(len(curr_members)):
    try:
        sheet.find(curr_members[i])
    except:
        sheet.update_cell(past_members_list[49].row,1,"0")
        sheet.update_cell(past_members_list[49].row,2,curr_members_contribution[i])
        sheet.update_cell(past_members_list[49].row,3,curr_members[i])
        sheet.update_cell(past_members_list[49].row,6,curr_days[i])

sleep(2)

driver.close()