import praw
import os
from datetime import datetime
import operator

def get_time_difference_in_hours(unix_timestamp):
    input_datetime = datetime.utcfromtimestamp(unix_timestamp)
    current_datetime = datetime.utcnow()
    time_difference = current_datetime - input_datetime
    hours_difference = time_difference.total_seconds() / 3600
    return hours_difference

def scrape_articles(sub, time, upvoteScore):
    reddit = praw.Reddit(
        client_id= os.getenv('RED_CLIENT_ID'),
        client_secret= os.getenv('RED_API_KEY'),
        password=os.getenv('RED_PASSWORD'),
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 "
                "Safari/537.36",
        username=os.getenv('RED_USERNAME')
    )
    news_array = []
    subreddit = reddit.subreddit(sub)
    j = 0
    for submission in subreddit.top(time_filter=time):
        if submission.score > upvoteScore:
            news_array.append({"title":submission.title, "link":submission.url, "sub_score":submission.score, "sub":sub, "time":get_time_difference_in_hours(submission.created_utc), "subscribers":subreddit.subscribers})
        j = j + 1
    return {"articles":news_array}

def scrape_memes(sub, time, upvote_score):
    reddit = praw.Reddit(
        client_id= os.getenv('RED_CLIENT_ID'),
        client_secret= os.getenv('RED_API_KEY'),
        password=os.getenv('RED_PASSWORD'),
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 "
                "Safari/537.36",
        username=os.getenv('RED_USERNAME')
    )
    subreddit = reddit.subreddit(sub)
    imageArray = []
    i=0
    for submission in subreddit.top(time_filter=time):
        if submission.score > upvote_score:
            if ".jpg" in submission.url or ".png" in submission.url:
                imageArray.append({"title":submission.title, "image":submission.url, "sub_score":submission.score, "sub":sub, "time":get_time_difference_in_hours(submission.created_utc), "subscribers":subreddit.subscribers})
        i += 1
    return {"memes":imageArray} 

def return_complete_array(object, obj_key):
    new_array = object[obj_key]
    for i in range(len(new_array)):
        score = float("{:.2f}".format((new_array[i]['subscribers'] / new_array[i]["sub_score"]) / new_array[i]["time"]))
        if score > 1:
            score = int(score)
        new_array[i]['score']  = score
    new_list = sorted(new_array, key=lambda d: d['score'], reverse=True) 
    return {obj_key:new_list} 


def full_scrape(articles):
    if articles:
        scrape_array = [scrape_articles("technews","week", 100), scrape_articles("tech", "week", 300), scrape_articles("technology", "day", 150), scrape_articles("computers", "day", 100), scrape_articles("hardware", "day", 100)]
        merged_scrape_list = []
        for scrape in scrape_array:
            merged_scrape_list += scrape['articles']
        return {'articles':merged_scrape_list}
    else:
        scrape_array = [scrape_memes("pcmasterrace", "week", 1000), scrape_memes("gaming", "week", 1000)]
        merged_scrape_list = []
        for scrape in scrape_array:
            merged_scrape_list += scrape['memes']
        return {'memes':merged_scrape_list}