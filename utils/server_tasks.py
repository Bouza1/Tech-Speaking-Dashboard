from apscheduler.schedulers.background import BackgroundScheduler
import json
from utils.scrape import scrape_memes, fullscrape

def task_2_run():
  append2Json(fullscrape(), "data/scrape_articles.json")
  print("Scraping.....")
#   append2Json(scrape_memes("pcmasterrace", "week", 5000), "data/scrape_memes.json")

  
def construct_scheduler():
  sched = BackgroundScheduler(daemon=True)
  sched.add_job(task_2_run, "interval", minutes = 60)
  return sched

def append2Json(article, filename):
  with open(filename, 'w') as json_file:
    json.dump(article, json_file, indent=4,  separators=(',',': '))



