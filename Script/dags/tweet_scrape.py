from datetime import datetime
import pandas as pd
import snscrape.modules.twitter as sntwitter



def tweet_scrape(keywords, start_date = None, end_date = datetime.now().date(), num_tweet = None):
    """
    This function use the snscrape library to scrape tweets that contain keywords within the start date to end date period. 
    
    Input: 
    keywords: An array of keywords. e.g. ['harry potter', 'spiderman']
    start_date: Start scraping tweets from this date. Default date is None. Date in the format of Year-Month-Day. e.g. 2022-03-08
    end_date: End scraping tweets from this date. Default date is the current date. Date in the format of Year-Month-Day. e.g. 2022-03-20
    num_tweet: Maximum number of tweets to scrape for each keyword. Default is None, meaning it will perform a greedy search. 
    
    Output: 
    tweets_df: A pandas dataframe that contains datetime, user id, tweet content, retweet count, like count, and keyword.

    Note: num_tweet is the maximum number of tweets that the function will scrape. 
    If the function cannot find more tweets, it will stop. 
    It is possible to end up a number less than num_tweet. 

    """
    
    ## Enter start date
    # start_year, start_month, start_day = map(int, input('Enter start year, month, and day: ').split())
    # start_date = datetime(start_year, start_month, start_day).strftime("%Y-%m-%d")

    ## Enter end date
    # end_year, end_month, end_day = map(int, input('Enter end year, month, and day: ').split())
    # end_date = datetime(end_year, end_month, end_day).strftime("%Y-%m-%d")

    # ## Enter keywords
    # keywords = []
    # while True:
    #     i = input("Enter search keywords (or Enter to quit): ")
    #     if not i:
    #         break
    #     keywords.append(i)

    # print(keywords)

    # Creating list to append tweet data to
    tweets_list = []

    ## For each keyword, search tweets
    for k in keywords:
        if start_date == None:
            search_scraper = '{} since:{}'.format(k, end_date)
        else:
            search_scraper = '{} since:{} until:{}'.format(k, start_date, end_date)

        # Using TwitterSearchScraper to scrape data and append tweets to list
        try:
            for i,tweet in enumerate(sntwitter.TwitterSearchScraper(search_scraper).get_items()):
                if num_tweet != None:
                    if i > num_tweet:
                        break
                # tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.retweetCount, tweet.likeCount, k])
                tweets_list.append([tweet.date, tweet.id, tweet.content, k])
        except:
            continue
    # tweets_df = pd.DataFrame(tweets_list, columns=['datetime', 'accountid', 'tweet','retweet_counts','like_counts','keyword'])
    tweets_df = pd.DataFrame(tweets_list, columns=['datetime', 'accountid', 'tweet','keyword'])
    return tweets_df




