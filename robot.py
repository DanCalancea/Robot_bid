import time
import datetime as dt
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait



def transformtime(time1): # transform timpul din formatul afisat de EBAY

    time1 = time1.replace('/', ',')
    time1 = time1.replace(' ', '')
    time1 = time1.replace(':', ',')
    timp_bid = time1.split(',')
    time_end = timp_bid[0] + '/' + timp_bid[1]
    today = datetime.now()
    year=today.year
    year=str(year)[2:]
    time_end+='/'+year+' '

    if timp_bid[3][2:] == 'PM':
        time_end += str(int(timp_bid[2]) + 12) + ':'
    else:
        time_end += timp_bid[2] + ':'

    time_end += timp_bid[3][:2] + ':00'

    timp = datetime.strptime(time_end, '%m/%d/%y %H:%M:%S')

    return timp


MYPASS = "AircroXXX@"   # Ebay password
MYUSER = "cala_XXX"     # Ebay user
EBAYITEM = "https://www.ebay.com/itm/195898352941?hash=item2d9c73a52d:g:oUYAAOSwpnZkuMOu&amdata=enc%3A" \
           "AQAIAAAAwBHG41DldfHHLHoHQdiTLh02RDZQBwkV%2BJ0%2FZbQSN6w5%2BZIxfrP81iOciO2EHTKEfeVPIHO%2FPLN1SHh7" \
           "09pWcX9LnbNCV0rP4hzNGJp2hbrP2vwoKrXJGjWYOd6c8ZNl3%2BV2vrhFnZjVyFBtvkryIagRVTQORfvNp5xNyUc3O%2F0O8XESC" \
           "wtcZX7paWXdua8Pua9g3oY1HwMQJxys8hsdKzscEinUi4wmwfYp4Jc6tnHtYuEI%2Fb0UcnDzUBuoZw8V4w%3D%3D%7Ctkp%3ABk9SR_jH-LWxYg"
MAXBID = '5'            # max bid
DEFAULTDELAY=2
SAFEBIDSEC=3            # a few seconds before the end we decide to bid
COMPENSATION=0          # we correct the seconds depending on the hardware and internet speed,
                        # it can have positive or negative values


driver = webdriver.Firefox()
driver.get(EBAYITEM)
time.sleep(DEFAULTDELAY)
time1 = driver.find_element(By.XPATH, "//span[@class='ux-timer__time-left']").text

secondestobid = int( (transformtime(time1) - datetime.now()).total_seconds())

print(' Total seconds to bid ',secondestobid)
# input()
secondestobid=30       # For testing only
time.sleep(secondestobid-6*DEFAULTDELAY-SAFEBIDSEC+COMPENSATION)   # try to bid in last 3 sec

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