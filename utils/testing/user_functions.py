from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


def construct_driver():
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def load_site(driver):
    driver.get("https://techspeaking.s4820791.repl.co/news/article/4")

def get_vote_text(driver, vote):
    vote_text = driver.find_element(By.ID, vote)
    return vote_text.text

def click_vote(driver, vote):
    vote_btn = driver.find_element(By.ID, vote)
    vote_btn.click()

def check_vote_works(driver, vote):
    if vote == 'like':
        pre_vote = get_vote_text(driver, 'like-score')
        time.sleep(2)
        click_vote(driver, 'like-btn')
        time.sleep(2)
        after_vote = get_vote_text(driver, 'like-score')
        if int(pre_vote)+1 == after_vote:
            print("True")
        else:
            print("False")


def user_func_tests():
    driver = construct_driver()
    load_site(driver)
    time.sleep(5)
    check_vote_works(driver, 'like')
                  
                  
    # like-score
    # like-btn

