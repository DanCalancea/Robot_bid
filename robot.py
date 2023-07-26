import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By


def nrdayofmonth(year, month):  # number of day month

    if ((month == 2) and ((year % 4 == 0) or ((year % 100 == 0) and (year % 400 == 0)))):
        return 29
    elif month == 2:
        return 28
    elif month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        return 31
    else:
        return 30


def transformtime(time1):  # transform timpul din formatul afisat de EBAY

    prima = time1.split(',')[0]
    wday = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, "Saturday": 5, 'Sunday': 6}
    today = datetime.now()
    year, month, day, dayweek = today.year, today.month, today.day, today.weekday()

    if time1[:5] == 'Today':
        time1 = time1.replace('Today', str(month) + '/' + str(day) + ',')
    if prima in wday.keys():
        if wday[prima] > dayweek:
            day += wday[prima] - dayweek
        else:
            day += 7 + wday[prima] - dayweek
        if day > nrdayofmonth(year, month):

            day = day - nrdayofmonth(year, month)
            month += 1
            if month == 13:
                month = 1
                year += 1
        time1 = time1.replace(prima + ',', str(month) + '/' + str(day) + ',')
    year = str(year)[2:]
    time1 = time1.replace('/', ',')
    time1 = time1.replace(' ', '')
    time1 = time1.replace(':', ',')
    timp_bid = time1.split(',')
    time_end = timp_bid[0] + '/' + timp_bid[1] + '/' + year + ' '

    if timp_bid[3][2:] == 'PM':
        time_end += str(int(timp_bid[2]) + 12) + ':'
    else:
        time_end += timp_bid[2] + ':'

    time_end += timp_bid[3][:2] + ':00'

    timp = datetime.strptime(time_end, '%m/%d/%y %H:%M:%S')

    return timp


MYPASS = "AircXXXX"  # Ebay password
MYUSER = "calXXXX6"  # Ebay user
EBAYITEM = "https://www.ebay.com/itm/354938773397?hash=item52a3ffdf95:g:VCEAAOSwf6xkv9fB"
MAXBID = '4'  # max bid
DEFAULTDELAY = 2
SAFEBIDSEC = 7  # a few seconds before the end we decide to bid
COMPENSATION = 0  # we correct the seconds depending on the hardware and internet speed,
                  # it can have positive or negative values


driver = webdriver.Firefox()
driver.get(EBAYITEM)
time.sleep(DEFAULTDELAY)
time1 = driver.find_element(By.XPATH, "//span[@class='ux-timer__time-left']").text
print(time1)
secondestobid = int((transformtime(time1) - datetime.now()).total_seconds())

print(' Total seconds to bid ', secondestobid, transformtime(time1))

# secondestobid=30       # For testing only

time.sleep(secondestobid - 6 * DEFAULTDELAY - SAFEBIDSEC + COMPENSATION)  # try to bid in last 3 sec

active_button = driver.find_element("link text", "Sign in")
active_button.click()
time.sleep(DEFAULTDELAY)

active_key = driver.find_element(By.ID, "userid")
active_key.send_keys(MYUSER)

active_button = driver.find_element(By.ID, "signin-continue-btn")
active_button.click()
time.sleep(DEFAULTDELAY)

active_key = driver.find_element(By.ID, "pass")
active_key.send_keys(MYPASS)
time.sleep(DEFAULTDELAY)

active_button = driver.find_element(By.ID, "sgnBt")
active_button.click()
time.sleep(DEFAULTDELAY)

active_button = driver.find_element(By.ID, "bidBtn_btn")  # apasa butonul de bid
active_button.click()
time.sleep(DEFAULTDELAY)

active_key = driver.find_element(By.ID, "s0-0-1-1-3-placebid-section-offer-section-price-10-textbox")
active_key.send_keys(MAXBID)
time.sleep(DEFAULTDELAY)

try:
    active_button = driver.find_element(By.XPATH, '//button[normalize-space()="Bid"]')
    active_button.click()
except:
    print('a larger amount has already been bid')

driver.quit()
