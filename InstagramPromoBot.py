import os  
import sys
import time
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

if not sys.version_info[0] == (3):
    print ("Error, I need python 3.*")
    exit()

if len(sys.argv) < 5:
    print ("python InstagramPromoBot.py <user> <pass> <promo URL> <@s per comment>")
    exit()

USER = sys.argv[1]
PASS = sys.argv[2]
PROMOURL = sys.argv[3]
QTDEMARCAR = int(sys.argv[4])
listOfSeguimores = []

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
    while found < totalSeguimores -1 and totalSeguimores > 1:
        driver.find_element_by_xpath("//body").send_keys(Keys.END)
        listOfSeguimores = firstDivOfPopUp.find_elements_by_xpath("//div//div//div//div//ul//div//li//div//div//div//div//a")
        found = len(listOfSeguimores)

arrobaSeguimores = []
for seguimores in listOfSeguimores:
    arrobaSeguimores.append("@" + seguimores.text)



driver.get(PROMOURL)
try:
    btComment = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'coreSpriteComment')]")))
finally:
    btComment.click()

subListOfSeguimores = [arrobaSeguimores[n:n+QTDEMARCAR] for n in range(0, len(arrobaSeguimores), QTDEMARCAR)]

try:
    inputComment = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//form//textarea")))
finally:
    for nSeguimores in subListOfSeguimores:
        if(len(nSeguimores) == QTDEMARCAR):
            try:
                inputComment = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//form//textarea")))
            finally:
                inputComment.send_keys(str(nSeguimores).replace("[", "").replace("'", "").replace("]", ""))
                inputComment.submit()
                time.sleep(1)


driver.quit()

print("DONE")