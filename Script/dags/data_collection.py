from create_database import create_job_tweet_tables, scrape_tweets
from datetime import datetime, timedelta
# from sqlite3 import connect
# import pandas as pd

if __name__ == '__main__':
    database = "tweets.db"
    create_job_tweet_tables(database)
    keywords = ['ukraine', 'russia']
    try:
        scrape_tweets(keywords,database = database, start_date = datetime.now().date() - timedelta(days=1), end_date = datetime.now().date(), num_tweet = 10)
    except:
        print('error')
    



