from utils.socials.post_2_LI import full_script_li
import json

def post_socials(article, cookie):
   if article['platform'] == "linkedin":
      if full_script_li(article, cookie):
         return True
      else: return False
   else:
      return False
   
def update_live_articles(id, json_url):
   with open(json_url) as openfile:
      full_json_object = json.load(openfile)
      live_articles = full_json_object['news']
      for article in live_articles:
         if str(article['id']) == str(id):
            article['linkedin'] = 1
   with open(json_url, 'w') as json_file:
      json.dump(full_json_object, json_file, indent=4,  separators=(',',': '))


