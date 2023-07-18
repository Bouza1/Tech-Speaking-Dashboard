from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import datetime
from utils.testing.links_testcases import links


def how_many_articles(driver):
    driver.get("https://techspeaking.s4820791.repl.co/news")
    time.sleep(3)
    articles = driver.find_elements(By.ID, "top-container")
    length = len(articles)
    return length

def create_article_objects(length):
    articles = []
    for i in range(1, length+1):
        link =  "https://techspeaking.s4820791.repl.co/news/article/" + str(i)
        article_obj = {"name": "Article " + str(i), "url":link, "title":"Article " + str(i)}
        articles.append(article_obj)
    return articles

def create_full_list(links, articles):
    for article in articles:
        links.append(article)
    return links

def construct_driver():
    chrome_options = Options()
    chrome_options.headless = True
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def check_page(driver, page):
    try:
        driver.get(page['url'])
        time.sleep(3)
        if driver.title == page['title']:
            return {"page":page['name'], "status": "Passed"}
        else:
            return {"page":page['name'], "status": "Failed", "Error":"Page Title Mismatch"}
    except:
        return {"page":page['name'], "status": "Failed", "Error":"Page Offline"}
    
def check_all_links(driver, pages):
    good_links = []
    bad_links = []
    for page in pages:
        result = check_page(driver, page)
        if result['status'] == "Passed":
            good_links.append(result)
        else:
            bad_links.append(result)
    return {"passed":good_links,"failed":bad_links}

def loop_all_links():
    driver = construct_driver()
    article_array = create_article_objects(how_many_articles(driver))
    full_list = create_full_list(links, article_array)
    results = check_all_links(driver, full_list)
    driver.quit()
    return results

def check_footer_link(driver, link):
    driver.get("https://bookingform.s4820791.repl.co")
    time.sleep(7)
    try:
        link_button = driver.find_element(By.ID, link['id'])
        link_button.click()
        time.sleep(4)
        get_url = driver.current_url
        time.sleep(4)
        if get_url == link['url']:
            return {link['name']:"Active"}
        else:
            return {link['name']:"Incorrect Link"}
    except:
        return {link['name'] : "Element Not Found!"}

def loop_all_footer_links(links):
    good_links = []
    bad_links = []
    driver = construct_driver()
    for button in links:
        result = check_footer_link(driver, button)
        if result[button['name']] == "Active":
            good_links.append(result)
        else:
            bad_links.append(result)
    return {"passed":good_links,"failed":bad_links}


# result = loop_all_footer_links(footer_links)
# print(result)