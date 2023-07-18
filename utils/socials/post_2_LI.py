import pickle
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException

load_dotenv('deets.env')

def construct_driver():
    chrome_options = Options()
    chrome_options.headless = True
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def load_linkedIN(driver, company):
    driver.get("https://www.linkedin.com" + company)

def load_cookies(driver, cookie):
    cookies = pickle.load(open(cookie, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

def post_da_post(driver, article):
    firstPostBtn = driver.find_element(By.XPATH, "//span[text()='Start a post']")
    firstPostBtn.click()
    time.sleep(4)
    textArea = driver.find_element(By.XPATH, "//div[@role='textbox']")
    textArea.click()
    textArea.send_keys(article['title'])
    textArea.send_keys(Keys.ENTER)
    textArea.send_keys(Keys.ENTER)
    textArea.send_keys(article['content'])
    textArea.send_keys(Keys.ENTER)
    textArea.send_keys(Keys.ENTER)
    textArea.send_keys("Read More: " + article['article_link'])
    time.sleep(20)
    submitBtn = driver.find_element(By.XPATH, "//span[text()='Post']")
    submitBtn.click()
    time.sleep(15)
    return post_successful(driver)


def post_successful(driver):
    try:
        driver.find_element(By.XPATH, "//span[text()='Post successful.']")
        return True
    except NoSuchElementException:
        return False

def full_script_li(article, cookie):
    try:
        driver = construct_driver()
        load_linkedIN(driver, "")
        time.sleep(5)
        load_cookies(driver, cookie)
        time.sleep(5)
        load_linkedIN(driver, os.getenv('COMPANY_SITE'))
        time.sleep(5)
        post_da_post(driver, article)
        return True
    except:
        return False


# full_script(post)


# def enter_dev_serial(driver, testcase):
#     dev_serial_input = driver.find_element(By.ID, "sn_inp")
#     dev_serial_input.send_keys(testcase['serial'])

# def enter_issues(driver, testcase):
#     issues_input = driver.find_element(By.ID, "issues_inp")
#     issues_input.send_keys(testcase['issues'])

# def enter_contact_prefs(driver, testcase):
#     contact_prefs_input = driver.find_element(By.ID, testcase['prefs'])
#     contact_prefs_input.click()

# def submit_repair_form(driver):
#     submit_btn = driver.find_element(By.ID, "submit-btn")
#     driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
#     time.sleep(1)
#     submit_btn.click();




# # ------------- Controlling Functions  ------------- #
# def cookieLoad(site):
#     cookies = pickle.load(open("cookies/" + site + ".pkl", "rb"))
#     for cookie in cookies:
#         print(cookie)
#         driver.add_cookie(cookie)

# def loadSite(site):
#     driver.get("https://www." + site + ".com")
#     cookieLoad(site)
#     driver.get("https://www." + site + ".com")

# # ------------- Linked IN  ------------- #
# def firstTimeLI(username, password):
#     time.sleep(6)
#     cookieBtn = driver.find_element(By.XPATH, "//button[contains(text(),'Accept')]")
#     cookieBtn.click()
#     time.sleep(2)
#     usernameInput = driver.find_element(By.NAME, "session_key")
#     usernameInput.send_keys(username)
#     passwordInput = driver.find_element(By.NAME, "session_password")
#     passwordInput.send_keys(password)
#     time.sleep(5)
#     loginBtn = driver.find_element(By.XPATH, "//*[@id='main-content']/section[1]/div/div/form/button")
#     loginBtn.click()
#     pickle.dump(driver.get_cookies(), open("cookies/cookies.pkl", "wb"))

# def postArticleLI(title, article):
#     driver.get("https://www.linkedin.com/company/91642186/admin/")
#     time.sleep(5)
#     firstPostBtn = driver.find_element(By.XPATH, "//span[text()='Start a post']")
#     firstPostBtn.click()
#     time.sleep(4)
#     textArea = driver.find_element(By.XPATH, "//div[@role='textbox']")
#     textArea.click()
#     textArea.send_keys(title)
#     textArea.send_keys(Keys.ENTER)
#     textArea.send_keys(article)
#     time.sleep(4)
#     submitBtn = driver.find_element(By.XPATH, "//span[text()='Post']")
#     submitBtn.click()

# def fullScriptLI(driver, title, article):
#     driver.get(dri)
#     time.sleep(5)
#     if os.path.exists('Tls/linkedIN.pkl'):
#         cookieLoad("linkedIN")
#     else:
# # this needs reconfiguring so that if username is false it wont run
#         firstTimeLI(False, False)
#     time.sleep(5)
#     postArticleLI(title, article)

# # ------------- Twitter ------------- #
# def postArticleTW(title, article):
#     time.sleep(5)
#     textArea = driver.find_element(By.XPATH, "//div[@role='textbox']")
#     textArea.click()
#     time.sleep(1)
#     textArea.send_keys(title)
#     textArea.send_keys(Keys.ENTER)
#     textArea.send_keys(article)
#     submitBtn = driver.find_element(By.XPATH, "//span[text()='Tweet']")
#     submitBtn.click()

# def fullScriptTW(title, article):
#     global driver

#     loadSite("twitter")
#     time.sleep(5)
#     postArticleTW(title, article)