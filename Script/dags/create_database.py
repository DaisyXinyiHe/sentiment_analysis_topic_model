from tweet_scrape import tweet_scrape
from datetime import datetime
import sqlite3
from sqlite3 import Error
import sqlalchemy as db

## Create connection to an existing database or create a new database if it does not exist
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    # finally:
    #     if conn:
    #         conn.close()
    return conn

######### Create tables within the database ######### 

## Function for creating table
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

## SQL commands for creating tables
## Two tables: 
## 1. Job status table track whether the job was done successfully
## 2. Tweets table is the tweets dataset
sql_create_jobstatus_table = """ CREATE TABLE IF NOT EXISTS job_status (
                                    id integer PRIMARY KEY,
                                    job_name text NOT NULL,
                                    job_date text,
                                    success text NOT NULL,
                                    error text
                                ); """

# sql_create_tweets_table = """CREATE TABLE IF NOT EXISTS tweets (
#                                 id integer PRIMARY KEY,
#                                 datetime text NOT NULL,
#                                 accountid integer,
#                                 tweet text,
#                                 retweet_counts integer,
#                                 like_counts integer,
#                                 keyword text NOT NULL,
#                                 job_id integer NOT NULL,
#                                 FOREIGN KEY (job_id) REFERENCES job_status (id)
#                             );"""

## old version
sql_create_tweets_table = """CREATE TABLE IF NOT EXISTS tweets (
                                id integer PRIMARY KEY,
                                datetime text NOT NULL,
                                accountid integer,
                                tweet text,
                                keyword text NOT NULL,
                                job_id integer NOT NULL,
                                FOREIGN KEY (job_id) REFERENCES job_status (id)
                            );"""


## Creating table
def create_job_tweet_tables(database):
    # create a database connection
    conn = create_connection(database)
    print(conn)

    # create tables
    if conn is not None:
        # create job status table
        create_table(conn, sql_create_jobstatus_table)

        # create tweetstable
        create_table(conn, sql_create_tweets_table)
    else:
        print("Error! cannot create the database connection.")


## Insert job into job table
def insert_job(conn, job_status):
    """
    Insert a new job into the job_status table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO job_status(job_name,job_date,success, error)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, job_status)
    conn.commit()
    return cur.lastrowid

## Insert tweet into tweet table
# def insert_tweet(conn, tweet):
#     """
#     Insert a new tweet into the job_status table
#     :param conn:
#     :param tweet:
#     """
#     sql = '''INSERT INTO tweets(datetime, accountid, tweet, retweet_counts, like_counts, keyword, job_id) VALUES(?,?,?,?,?,?,?) '''
#     cur = conn.cursor()
#     cur.execute(sql, tweet)
#     conn.commit()

## Insert tweet into tweet table --old version
def insert_tweet(conn, tweet):
    """
    Insert a new tweet into the job_status table
    :param conn:
    :param tweet:
    """
    sql = '''INSERT INTO tweets(datetime, accountid, tweet, keyword, job_id) VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, tweet)
    conn.commit()

######## Scrape tweets and add data into database ########

## make all datetime object to string object so SQL can accept the datatype
def date_to_string(datetime_obj):
    return datetime_obj.strftime("%m/%d/%Y, %H:%M:%S")
   

## scrape tweets and save data into database
def scrape_tweets(keywords,database = 'tweets.db', start_date = None, end_date = datetime.now().date(), num_tweet = None):
    success = ''
    error = ''
    tweet_df = []
    connection = create_connection(database) ## connect with database

    ## Scrape tweets
    tweet_df = tweet_scrape(keywords, start_date = start_date, end_date = end_date, num_tweet = num_tweet)
    tweet_df['datetime'] = tweet_df['datetime'].apply(date_to_string)
    if len(tweet_df) == 0:
        success = 'N'
        error = 'tweet scraping error'
        print(error)
    else:
        success = 'Y'

    if connection != None:
        ## log job status
        job_status = ('scrape_tweets', datetime.now(), success, error)
        job_id = insert_job(connection, job_status)
        tweet_df['job_id'] = job_id

        ## log tweets to tweets table
        for ind,row in tweet_df.iterrows():   
            insert_tweet(connection, tuple(row))

        # for row in connection.execute('SELECT * FROM tweets'):
        #     print(row)
    else:
        print('connection error')
    

