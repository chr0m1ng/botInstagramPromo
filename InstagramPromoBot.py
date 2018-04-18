import os  
import sys
import time
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



if len(sys.argv) < 4:
    print ("./python InstagramPromoBot.py <user> <pass> <promo URL>")
    exit()


# def scrollTillOpenAllFollowers(total, elementToScroll):
#     SCROLL_PAUSE_TIME = 0.5
#     found = 0
#     listOfSeguimores = []
#     firstDivOfPopUp.click()
#     while found < total:
#         # Scroll down to bottom
#         elementToScroll.send_keys(Keys.END)
#         listOfSeguimores = elementToScroll.find_elements_by_xpath("//div//div//div//div//ul//div//li")
#         found = len(listOfSeguimores)

#         # Wait to load page
#         time.sleep(SCROLL_PAUSE_TIME)
#     return listOfSeguimores


USER = sys.argv[1]
PASS = sys.argv[2]
PROMOURL = sys.argv[3]

chrome_options = Options()  

chrome_options.binary_location = "C:\\Users\\Dev\\AppData\\Local\\Google\\Chrome SxS\\Application\\chrome.exe"
chrome_options.add_argument("--incognito")  

driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get("https://www.instagram.com/accounts/login/")

try:
    userInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
    passInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
finally:    
    userInput.send_keys(USER)
    passInput.send_keys(PASS)
    passInput.submit()

try:
    btOpenProfile = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'coreSpriteDesktopNavProfile')]")))
finally:
    btOpenProfile.click()

try:
    btOpenSeguimores = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/%s/followers/')]" % (USER))))
finally:
    totalSeguimores = int(btOpenSeguimores.find_element_by_tag_name("span").text)
    btOpenSeguimores.click()
    
try:
    firstDivOfPopUp = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@role, 'dialog')]")))
finally:
    firstDivOfPopUp.click()
    found = 0
    while found < totalSeguimores - 1:
        driver.find_element_by_xpath("//body").send_keys(Keys.END)
        listOfSeguimores = firstDivOfPopUp.find_elements_by_xpath("//div//div//div//div//ul//div//li")
        found = len(listOfSeguimores)

driver.get(PROMOURL)
try:
    btComment = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'coreSpriteComment')]")))
finally:
    btComment.click()
    
driver.quit()