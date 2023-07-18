from utils.socials.fb import post_2_fb
from utils.socials.post_2_LI import full_script_li
import os
import json

def post_socials(article, cookie):
   if article['platform'] == "linkedin":
      if full_script_li(article, cookie):
         return True
      else: 
         return False
   elif article['platform'] == "facebook":
         return_statement = post_2_fb(os.getenv('FB_TOKEN'), os.getenv('FB_PAGE_ID'), article)
         print(json.dumps(return_statement, indent=4))
         if return_statement != False:
            return True
         else:
            return False
   else:
      return False
   
def update_live_articles(id, platform, json_url):
   with open(json_url) as openfile:
      full_json_object = json.load(openfile)
      live_articles = full_json_object['news']
      for article in live_articles:
         if str(article['id']) == str(id):
            article[platform] = 1
   with open(json_url, 'w') as json_file:
      json.dump(full_json_object, json_file, indent=4,  separators=(',',': '))


