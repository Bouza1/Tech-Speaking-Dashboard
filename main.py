from flask import Flask, render_template, request
import json
import os
from utils.post_engine import post_socials, update_live_articles
from utils.rewrite import append_rewite_2_live_articles, rewrite_4_socials
from utils.server_tasks import construct_scheduler
from utils.testing.test_suite_server import run_this_test
from utils.add_article import format_article_obj, append_Article_2_Json

app = Flask(__name__)

sched = construct_scheduler()
sched.start()

@app.route('/')
def home_page():
    return render_template("home.html")

@app.route('/testing')
def testing_page():
  return render_template("testing.html")

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

@app.route('/new_content')
def content_page():
   return render_template("content.html")

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

@app.route("/social_mgmt")
def social_page():
   return render_template('social.html')

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
    one_big_string = ' '.join(article_object['content'])
    post = rewrite_4_socials(one_big_string)
    article_object['post'] = [post]
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
      update_live_articles(article['id'], json_url)
      return {"message":"Success! Posted!"}
    else:
      return {"message":"Failed! Not Posted"}

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




# @app.route("/api/admin/schedule_post", methods=['PUT', 'GET'])
# def schedule_post():
#   if request.is_json:
#     print(request)
#     site_root = os.path.realpath(os.path.dirname(__file__))
#     json_url = os.path.join(site_root, "data", "temp.json")
#     json_object = request.get_json()
#     append_2_temp_file(json_object, json_url)
#     # # update_live_articles(json_object['id'], json_url2)
#     return {"message":"Success"}
#   else:
#     return {"message":"Error Scheduling Post"}

#     return render_template('index.html')


# @app.route("/api/admin/download_schedule", methods=['POST'])
# def download_schedule():
#   if request.method == 'POST':
#     path = os.path.join(os.getcwd(), 'data/temp.json')
#     return send_file(path, as_attachment=True)
