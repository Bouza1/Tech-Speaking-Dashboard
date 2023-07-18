from apscheduler.schedulers.background import BackgroundScheduler
import json
from utils.content.scrape import return_complete_array, full_scrape

def task_2_run():
  pre_object = full_scrape(True)
  news_array = return_complete_array(pre_object, 'articles')
  append2Json(news_array, "data/scrape_articles.json")
  pre_memes= full_scrape(False)
  memes_array = return_complete_array(pre_memes, 'memes')
  append2Json(memes_array, "data/scrape_memes.json")
  print("Scraping.....")

def construct_scheduler():
  sched = BackgroundScheduler(daemon=True)
  sched.add_job(task_2_run, "interval", minutes = 120)
  return sched

def append2Json(article, filename):
  with open(filename, 'w') as json_file:
    json.dump(article, json_file, indent=4,  separators=(',',': '))
