from flask import Flask, render_template, request, send_file
import json
import os
from utils.socials.edit_photos import screen_shot_photo
from utils.content.live_articles import format_live_articles_4_site
from utils.socials.post_engine import post_socials, update_live_articles
from utils.socials.rewrite import append_rewite_2_live_articles, rewrite_4_socials
from utils.server_tasks import construct_scheduler
from utils.testing.test_suite_server import run_this_test
from utils.content.add_article import format_article_obj, append_Article_2_Json
from utils.content.upload import full_script_upload

app = Flask(__name__)

sched = construct_scheduler()
sched.start()

@app.route('/')
def home_page():
    return render_template("home.html")

@app.route('/testing')
def testing_page():
  return render_template("testing.html")

@app.route('/website_mgmt')
def website_page():
   return render_template("website.html")

@app.route("/social_mgmt")
def social_page():
   return render_template('social.html')

@app.route("/content_engine")
def content_engine_page():
  return render_template("content_engine.html")

@app.route('/api/get_testing_results', methods=['GET', 'POST'])
def return_test_results():
  if request.method == 'GET':
    site_root = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(site_root, "data", "latest_results.json")
    full_json_object = []
    with open(json_url) as openfile:
        full_json_object = json.load(openfile)
    news_articles = full_json_object['results']
    return news_articles[::-1] 

@app.route('/api/get_test_dates', methods=['GET', 'POST'])
def return_test_dates():
  if request.method == 'GET':
    site_root = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(site_root, "data", "latest_results.json")
    full_json_object = []
    with open(json_url) as openfile:
        full_json_object = json.load(openfile)
    test_dates = full_json_object['last_ran']
    return test_dates

@app.route("/api/run_test", methods=['PUT', 'GET'])
def run_test():
  if request.is_json:
    test = request.get_json()
    site_root = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(site_root, "data", "latest_results.json")
    result = run_this_test(test['Test'], json_url)
    if result['failed'] == []:
      return {"Message": "All Tests Passed", "Alert":"success"}
    else:
       return {"Message": "Error! Downloading Log!", "Alert":"danger"}

@app.route("/api/add_article", methods=['PUT', 'GET'])
def add_article():
  message = {"message":"Failed"}
  if request.method == 'PUT':
    req = request.get_json()
    site_root = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(site_root, "data", "live_articles.json")
    unformatted_article_obj = req['article']
    formatted_article = format_article_obj(unformatted_article_obj, json_url)
    append_Article_2_Json(formatted_article, json_url)
    message = {"message":"Success"}
    site_root = os.path.realpath(os.path.dirname(__file__))
    format_live_articles_4_site(site_root)
    full_script_upload(site_root)
  return message

@app.route("/api/get_new_articles", methods=['GET', 'POST'])
def get_new_articles():
  if request.method == "GET":
    site_root = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(site_root, "data", "scrape_articles.json")
    full_json_object = []
    with open(json_url) as openfile:
        full_json_object = json.load(openfile)
    scraped_news = full_json_object['articles']
    return scraped_news

@app.route("/api/get_new_memes", methods=['GET', 'POST'])
def get_new_memes():
  if request.method == "GET":
    site_root = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(site_root, "data", "scrape_memes.json")
    full_json_object = []
    with open(json_url) as openfile:
        full_json_object = json.load(openfile)
    scraped_memes = full_json_object['memes']
    return scraped_memes

@app.route("/api/get_live_articles", methods=['POST', 'GET'])
def pull_articles():
  if request.method == "GET":
    site_root = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(site_root, "data", "live_articles.json")
    full_json_object = []
    with open(json_url) as openfile:
        full_json_object = json.load(openfile)
    news_articles = full_json_object['news']
    return news_articles[::-1]

@app.route("/api/rewrite_4_socials", methods=['PUT', 'GET'])
def rewrite_article():
  if request.is_json:
    json_object = request.get_json()
    article_object = return_object_using_id(int(json_object['id']))
    if article_object['social_post_text'] != "":
      return article_object
    else :
      one_big_string = ' '.join(article_object['content'])
      post = rewrite_4_socials(one_big_string)
      article_object['social_post_text'] = post
      site_root = os.path.realpath(os.path.dirname(__file__))
      json_url = os.path.join(site_root, "data", "live_articles.json")
      append_rewite_2_live_articles(json_url, int(json_object['id']), post)
      return article_object
  else:
      return "Hello"
  
@app.route("/api/post_article_2_socials", methods=['PUT', 'GET'])
def post_2_socials():
  if request.is_json:
    article = request.get_json()
    site_root = os.path.realpath(os.path.dirname(__file__))
    cookie = os.path.join(site_root, 'utils', 'socials', 'cookies', 'linkedIN.pkl')
    json_url = os.path.join(site_root, "data", "live_articles.json")
    if post_socials(article, cookie):
      update_live_articles(article['id'], article['platform'], json_url)
      return {"message":"Success! Posted!"}
    else:
      return {"message":"Failed! Not Posted"}
    
@app.route("/api/display_img/<int:id>", methods=['GET', 'POST'])
def return_img(id):
  if request.method == "GET":
    article = return_object_using_id(id)
    return render_template("img_view.html", article=article)
  
@app.route("/api/display_image/screenshot", methods=['GET', 'PUT'])
def screenshot():
  if request.is_json:
    site_root = os.path.realpath(os.path.dirname(__file__))
    url_obj = request.get_json()
    id = url_obj['id'].replace('"', '') 
    screen_shot_photo(url_obj['url'], id, site_root)
    return {"message":"success"}

@app.route("/api/download_articles", methods=['GET', 'POST'])
def download_articles():
  if request.method == 'POST':
    site_root = os.path.realpath(os.path.dirname(__file__))
    format_live_articles_4_site(site_root)
    path = os.path.join(os.getcwd(), 'data/temp.json')
    return send_file(path, as_attachment=True)

def return_object_using_id(id):
  site_root = os.path.realpath(os.path.dirname(__file__))
  json_url = os.path.join(site_root, "data", "live_articles.json")
  article = False
  with open(json_url) as openfile:
    full_json_object = json.load(openfile)
    news_articles = full_json_object['news']
    for i in range(len(news_articles)):
      if news_articles[i]['id'] == id:
        article =  news_articles[i]
  return article


app.run(host='0.0.0.0', port=81)



