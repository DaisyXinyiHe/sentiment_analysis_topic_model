import pandas as pd
import numpy as np
import re
import string
from sqlite3 import connect
import umap
import hdbscan
from bertopic import BERTopic
import matplotlib.pyplot as plt
from sentiment_analysis import predict_sentiments

def load_data(database):
    conn = connect(database)
    dataset = pd.read_sql('SELECT * FROM tweets', conn)
    return dataset

## Tweet cleaning functions

## Change all tweets to lowercase
def lower_case(tweet):
  return tweet.lower()

## Remove punctuation
def remove_punctuation(tweet):
  PUNCT_TO_REMOVE = string.punctuation+'’'+'「'+'」'
  return tweet.translate(str.maketrans('', '', PUNCT_TO_REMOVE))

# ## Filter stop words
# def filter_stopwords(tweet):
#   filtered = ''
#   stop_words = stopwords.words('english')
#   stop_words.append('im')
#   stop_words = set(stop_words)
#   word_tokens = word_tokenize(tweet)
#   filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
#   filtered = ' '
#   filtered =filtered.join(filtered_sentence)
#   return filtered


## Remove unnecessary symbols
def clean(tweet):
  # tweet = " ".join(filter(lambda x:x[0]!='@', tweet.split())) # remove @mention
  tweet = re.sub(r'@','', tweet) # remove @ symbol
  tweet = re.sub(r'#','', tweet) # remove hastag symbol
  tweet = re.sub(r'https?:\/\/\S+','', tweet) # remove hyperlink
  tweet = re.sub(r'rt[\s]+','', tweet) # remove 'RT'
  # tweet = remove_punctuation(tweet)
#   tweet = filter_stopwords(tweet)
  return tweet

# ## replace emoji and emoticons to words
# def convert_emoji(tweet):
#   for emo in UNICODE_EMO:
#     if emo in tweet:
#       tweet = tweet.replace(emo, UNICODE_EMO[emo])
#     tweet = tweet.lower()
#     tweet = tweet.replace(':', '')
#     # tweet = tweet.replace('_', ' ')
#   return tweet

# ## Take away the keywords for search in tweets
# def take_away_keyword(tweet):
#   for k in search_word:
#     if k in tweet:
#       tweet = tweet.replace(k, '')
#   return tweet

# ## Connect keywords as one word
# def connect_keyword(tweet, keyword):
#   keyword_connected = keyword.replace(' ', '_')
#   if keyword in tweet:
#     tweet = tweet.replace(keyword, keyword_connected)
#   return tweet

def get_date(date_time):
  date_time = date_time.split(' ')
  return date_time[0]

if __name__ == '__main__':

  ## Load data
  tweets = load_data('tweets.db')
  # print(tweets.columns)
  ## Get dates
  tweets['date'] = tweets.datetime.apply(get_date)
  ## Clean tweets
  tweets['tweet_processed'] = tweets['tweet'].apply(lower_case)
  tweets['tweet_processed']  =tweets['tweet'].apply(clean)  
  ## drop duplicates  
  tweets = tweets.drop(tweets.loc[tweets['tweet'].duplicated()].index)
  ## reset index
  tweets = tweets.reset_index(drop=True)
  ## drop empty tweets
  empty_tweet = []
  for t in range(len(tweets)):
      if len(tweets.tweet.iloc[t])==0:
          empty_tweet.append(t)
      tweets = tweets.drop(index = empty_tweet)
      tweets= tweets.reset_index(drop=True)

  ## Get dates
  dates = tweets['date'].apply(lambda x: pd.Timestamp(x)).to_list()
  
  ## Get tweets as text
  text = tweets.tweet_processed.to_list()

  ## Topic Modeling
  umap_model = umap.UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine', random_state=40)
  topic_model = BERTopic(min_topic_size=15, n_gram_range=(1,3), verbose=True, umap_model=umap_model)
  topics, probabilities = topic_model.fit_transform(text)

  ## show topic
  fig = topic_model.visualize_topics()
  # fig.show()

  ## topic over time
  topic_over_time = topic_model.topics_over_time(text, topics, dates)
  fig1 = topic_model.visualize_topics_over_time(topic_over_time, topics=list(np.arange(0,len(topics))))
  # fig1.show()

  ## topic by class
  tweets = predict_sentiments(tweets)
  classes = [s for s in tweets.sentiment]
  topics_per_class = topic_model.topics_per_class(text, topics, classes=classes)
  fig2 = topic_model.visualize_topics_per_class(topics_per_class)
  # fig2.show()





  
