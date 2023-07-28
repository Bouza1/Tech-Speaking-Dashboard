from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException

def construct_driver():
    chrome_options = Options()
    chrome_options.headless = True
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def load_site(driver):
    driver.get("https://techspeaking.s4820791.repl.co/login")

def login(driver):
    username = driver.find_element(By.ID, "username")
    username.send_keys("bouza1")
    password = driver.find_element(By.ID, "password")
    password.send_keys("bouza1")
    time.sleep(2.3)
    submit_btn = driver.find_element(By.ID, "submit")
    submit_btn.click()

def upload_file(driver, file):
    file_upload = driver.find_element(By.ID, "file_upload")
    file_upload.send_keys(file)
    upload_btn = driver.find_element(By.ID, "upload_btn")
    upload_btn.click()

def full_script_upload(site_root):
    driver = construct_driver()
    load_site(driver)
    time.sleep(5.1)
    login(driver)
    time.sleep(5.3)
    file = os.path.join(site_root, "data", "temp.json")
    upload_file(driver, file)
    time.sleep(1)
    driver.quit()
