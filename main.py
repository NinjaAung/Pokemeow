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
sheet  = client.open_by_key("1THmPwG9om9FSzDfL8gYYUqCrXjie1Dtl-5YVta7eMSQ").sheet1

# Config
config   = dotenv_values(".env")
USERNAME = config["USER_NAME"]
PASSWORD = config["USER_PASSWORD"]

# Messages
start_message   = "Starting Count!"
pokemeow        = ";clan members"
pokemeow_next   = "next"
pruning         = "eli purge 5"
REWARD=True

# Vaiables
curr_members              = []
curr_members_join_date    = []
curr_members_contribution = []

driver   = webdriver.Chrome("./drivers/chromedriver")
keyboard = Controller()
driver.get("https://discord.com/channels/719694038088810506/797292197811585066")
keyboard = Controller()

def sanitazing(members:list,contrib:list):
    for i in range(0,len(members)):
        members[i]  = members[i][3:].strip()
        contrib[i]  = re.sub(r"\|.*","",contrib[i]).strip()

def typing(message: str,start_in:int=0,start_next:int=0):
    sleep(start_in)
    for letter in message:
        keyboard.press(letter)
        keyboard.release(letter)

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    sleep(start_next)

def data_recording(contribution_cell_range:list,member_cell_range:list,days_cell_range:list):
    for i in range(0,len(curr_members)):
        timedelta = datetime.now() - datetime.fromisoformat(curr_members_join_date[i])
        if curr_members[i] == "": # Change or remove this
            curr_members[i] = ":fries:"
        if timedelta.days <= 0:
            days = 1
        else:
            days = timedelta.days
        days_cell_range[i].value         = days
        contribution_cell_range[i].value = curr_members_contribution[i]
        member_cell_range[i].value       = curr_members[i]


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

    typing(pokemeow_next,1)

typing(pruning,1)
sleep(2)
driver.close()

data_exist = bool(sheet.cell(2,6).value)
if data_exist:
    member_contribution_dic = {}
    new_past_contribution = sheet.range('D2:D51')
    curr_contribution     = sheet.range('E2:E51')
    curr_members_list     = sheet.range('F2:F51')

    past_members_list = sheet.range('F2:F51')
    cell_list_days    = sheet.range('I2:I51')

    for i in range(0,len(curr_contribution)): # Update yesterday
        new_past_contribution[i].value = curr_contribution[i].value
    sheet.update_cells(new_past_contribution,'USER_ENTERED')
    print('New Yesterday Added ✅')

    data_recording(curr_contribution,curr_members_list,cell_list_days)
    for i in range(0,len(curr_members_contribution)):
        member_contribution_dic[curr_members_list[i].value] = curr_members_contribution[i]

    print("Checking if Members Left:")
    for i in range(len(past_members_list)): # Deleting Members
        if not past_members_list[i].value in curr_members:
            if past_members_list[i].value == "":
                break
            sheet.update_cell(past_members_list[i].row,past_members_list[i].col-2,"") # Yesterday
            sheet.update_cell(past_members_list[i].row,past_members_list[i].col-1,"") # Today
            sheet.update_cell(past_members_list[i].row,past_members_list[i].col,"")   # Member
            print(f'\t{past_members_list[i].value} Deleted ✅')
        else:
            member_cell = sheet.find(past_members_list[i].value,None,6)
            sheet.update_cell(member_cell.row,member_cell.col-1,member_contribution_dic[past_members_list[i].value])

    sheet.sort((5,"des"),range="D2:F51")

    print("Checking if Members Joined:")
    for i in range(0,len(curr_members)): # Adding Members
        try:
            sheet.find(curr_members[i],None,6)
        except:
            sheet.update_cell(past_members_list[49].row,past_members_list[i].col-2,"0")                               # Yesterday
            sheet.update_cell(past_members_list[49].row,past_members_list[i].col-1,str(curr_members_contribution[i])) # Today
            sheet.update_cell(past_members_list[49].row,past_members_list[i].col,str(curr_members[i]))                # Member
            sheet.sort((5,"des"),range="D2:F51")
            print(f'\t{past_members_list[i].value} Added ✅')

    sheet.update_cells(cell_list_days,'USER_ENTERED')
    print("Days Updated")

    if REWARD:
        if not datetime.today().weekday() in [5,6]:
            print("not yet")


























    
else:
    cell_list_contribution  = sheet.range('E2:E51')
    cell_list_member        = sheet.range('F2:F51')
    cell_list_days          = sheet.range('I2:I51')

    data_recording(cell_list_contribution,cell_list_member,cell_list_days)

    sheet.update_cells(cell_list_contribution,'USER_ENTERED')
    print("Members Added ✅")
    sheet.update_cells(cell_list_member,'USER_ENTERED')
    print("Contributions Added ✅")
    sheet.update_cells(cell_list_days,'USER_ENTERED')
    print("Stay Added ✅")