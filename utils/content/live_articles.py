import json
import os

def format_live_articles_4_site(site_root):
    news_array = []
    json_url = os.path.join(site_root, "data", "live_articles.json")
    with open(json_url) as openfile:
        full_json_object = json.load(openfile)
        news_articles = full_json_object['news']
    for article in news_articles:
        formatted_article_obj = {"id":article['id'], "title":article['title'], "content":article['content'], "imagelink":article['imagelink'], "livelink":article['livelink'], "like":article['like'], "dislike": article['like']}
        news_array.append(formatted_article_obj)
    json_object = {"news":news_array}
    json_url = os.path.join(site_root, "data", "temp.json")
    with open(json_url, 'w') as json_file:
        json.dump(json_object, json_file, indent=4,  separators=(',',': '))




