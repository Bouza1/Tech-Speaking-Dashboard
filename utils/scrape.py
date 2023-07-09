import praw
import os

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
            news_array.append({"title":submission.title, "link":submission.url, "score":submission.score, "sub":sub})
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
                imageArray.append({"title":submission.title, "image":submission.url, "score":submission.score})
        i += 1
    return {"memes":imageArray} 


def fullscrape():
    scrape_array = [scrape_articles("technews","day", 10),scrape_articles("tech", "day", 50),scrape_articles("Futurology", "day", 150), scrape_articles("technology", "day", 150), scrape_articles("computers", "day", 100), scrape_articles("hardware", "day", 100)]
    merged_scrape_list = []
    for scrape in scrape_array:
        merged_scrape_list += scrape['articles']
    return {'articles':merged_scrape_list}