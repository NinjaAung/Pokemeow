# Pokemeow

Pokemeow is a script use to interact with the Pokemeow Bot for clan statistics tracking `average catch rate`,`daily catch` and`days`. This project uses selenium, so if you need a chrome driver go [here](https://chromedriver.chromium.org/downloads) [You can use any driver you want].

## Instructions

Download with [zip](https://github.com/NinjaAung/Pokemeow/archive/main.zip) or with cli:

```bash
git clone https://github.com/ninjaaung
```

Create and add to .env

```env
USER_NAME=       # Discord Username
USER_PASSWORD=   # Discord Password
CALC_CHANNEL=    # Channel Url to do calculations in (Use discord on your browser to find this)
GOOGLE_SHEET_ID= # ID of Google sheet (Found in URL)
```

Install all modules

```bash
pip3 install -r requirements.txt
```
***On discord please make sure your calc channel is always empty!***<br>
Then make sure you add your creds.json from google service account and all you have to do is run

```bash
python3 main.py
```
