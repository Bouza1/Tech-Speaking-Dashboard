import json 

def format_article_obj(unformatted, json_url):
  id = add_Id_2_Article(json_url)
  formatted_article = {
    "id": id,
    "title":unformatted['title'],
    "content":unformatted['content'],
    "imagelink":unformatted['imagelink'],
    "livelink": "https://techspeaking.s4820791.repl.co/news/article/" + str(id),
    "linkedin": 0,
    "scheduled": 0,
    "like":0,
    "dislike":0,
    "social_post_text": "",
    "instagram": 0,
    "facebook": 0,
    "twitter": 0
  }
  return formatted_article

def add_Id_2_Article(json_url):
  with open(json_url) as openfile:
    full_json_object = json.load(openfile)
    news_articles = full_json_object['news']
  return len(news_articles) + 1

def append_Article_2_Json(article, json_url):
  with open(json_url) as openfile:
    full_json_object = json.load(openfile)
    news_articles = full_json_object['news']
    news_articles.append(article)
  with open(json_url, 'w') as json_file:
    json.dump(full_json_object, json_file, indent=4,  separators=(',',': '))


