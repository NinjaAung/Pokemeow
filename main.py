from oauth2client.service_account   import ServiceAccountCredentials
from pynput.keyboard                import Key, Controller
from selenium                       import webdriver
from dotenv                         import dotenv_values
from datetime                       import datetime
from time                           import sleep
import gspread
import re

# Config
config   = dotenv_values(".env")
USERNAME = config["USER_NAME"]
PASSWORD = config["USER_PASSWORD"]
CHANNEL  = config["CALC_CHANNEL"]
SHEET    = config["GOOGLE_SHEET"]

# Google Creds
scope  = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/spreadsheets']
creds  = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
client = gspread.authorize(creds)
sheet  = client.open_by_key(SHEET).sheet1

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

try: 
    driver   = webdriver.Chrome("./drivers/chromedriver")
except:
    print("Incompatable Version: Refer to https://stackoverflow.com/questions/38833589/oserror-errno-8-exec-format-error-selenium")
    print(f"\n\n {sys.exc_info()}")
    exit()

keyboard = Controller()
driver.get(str(CHANNEL))
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
typing(pokemeow,2)


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
    member_left_list = []
    update = []
    for i in range(len(past_members_list)): # Deleting Members
        cell = past_members_list[i]
        if not cell.value in curr_members:
            if cell.value == "":
                break
            for i in range(0,3):
                member_left_list.append(gspread.models.Cell(cell.row,cell.col-i,""))
            print(f'\t{cell.value} Deleted ✅')
        else:
            cell = sheet.find(past_members_list[i].value,None,6)
            cell_today = gspread.models.Cell(cell.row,cell.col-1,member_contribution_dic[past_members_list[i].value])
            update.append(cell_today)

    if member_left_list:
        sheet.update_cells(member_left_list,'USER_ENTERED')
    sheet.update_cells(update, 'USER_ENTERED')
    sheet.sort((5,"des"),range="D2:F51")

    print("Checking if Members Joined:")
    member_added = 1
    past_members = [i.value for i in past_members_list]
    update = []
    for i in range(0,len(curr_members)): # Adding Members
        cell = past_members_list[i]
        if not curr_members[i] in past_members:
            empty = len(past_members) - member_added
            cell_list = sheet.range(f"D{empty}:F{empty}")
            cell_list[0].value = "0"                            # Yesterday
            cell_list[1].value = curr_members_contribution[i]   # Today
            cell_list[2].value = curr_members[i]                # Member
            member_added += 1
            update += cell_list
            print(f'\t{past_members_list[i].value} Added ✅')
    if update:
        sheet.update_cells(update,'USER_ENTERED')
    sheet.sort((5,"des"),range="D2:F51")
    sheet.update_cells(cell_list_days,'USER_ENTERED')
    print("Days Updated")

    if REWARD:
        if not datetime.today().weekday() in [5,6]:
            Daily_Catch = sheet.range('G2:G51')
            print("Congrats")
            for i in range(0,len(Daily_Catch)):
                if int(Daily_Catch[i].value.replace(",","")) >= 1500:
                    print(sheet.cell(Daily_Catch[i].row,Daily_Catch[i].col-1).value)
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