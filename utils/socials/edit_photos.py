from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image
import os
import json

def construct_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def screen_shot_photo(url, id, site_root):
    folder_location = os.path.join(site_root, "static", "article_imgs_social")
    driver = construct_driver()
    driver.get(url)
    element = driver.find_element(By.ID, 'screenshot_me')
    location = element.location
    size = element.size
    temp_name = os.path.join(folder_location, "shot.png")
    driver.save_screenshot(temp_name)
    driver.quit()
    x = location['x']
    y = location['y']
    w = size['width']
    h = size['height']
    width = x + w
    height = y + h
    im = Image.open(temp_name)
    im = im.crop((int(x), int(y), int(width), int(height)))
    simp_filename = id +'.png'
    filename = os.path.join(folder_location, simp_filename)
    im.save(filename)
    location = "static/article_imgs_social/" + str(id) + ".png"
    update_live_articles(site_root, id, location)

def update_live_articles(site_root, id, location):
    json_url = os.path.join(site_root, "data", "live_articles.json")
    with open(json_url) as openfile:
        full_json_object = json.load(openfile)
        news_articles = full_json_object['news']
        for article in news_articles:
            if str(article['id']) == str(id):
                article.update({'social_post_img':location})
    with open(json_url, 'w') as json_file:
        json.dump(full_json_object, json_file, indent=4,  separators=(',',': '))

