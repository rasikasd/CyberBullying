from django.shortcuts import render
from .models import Profile
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
import re

ACCESS_TOKEN = '1206572403309965313-ZDeZ14s1m1WxZr8f9gpHHPwNzmWDpq'
ACCESS_TOKEN_SECRET = 'nJvwYjNNn5QZmpoOQieOB4WDx8dJfSGrn9P7GxXGMmem9'
CONSUMER_KEY = 'Z1iHhc5Gw34CHRrftyDtTNBf1'
CONSUMER_SECRET = 'OCV2x85aB6XZoIwIit7JeIVovIP2YpN3rXVv63KcrRgUobP8Zf'

def home(request):
    context = {
        'profile': Profile.objects.all()
    }
    return render(request, 'detection/home.html', context)


def about(request):
    return render(request, 'detection/about.html', {'title': 'About'})


def moderate(request):
    return render(request, 'detection/moderate.html', {'title': 'Moderate'})



# # # # # Twitter Clients # # # # #
class TwitterClient():
    def __init__(self,twitter_user = None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        
        self.twitter_user = twitter_user
    
    def get_twitter_client_api(self):
        return self.twitter_client
    
    ## Display the tweets of any user timeline ##   
    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline,id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets
    
     ## Display the tweets of any user friends timeline ##
    def get_friend_list(self,num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends,id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list
    
    ## Display the tweets of your home timeline ##
    def get_home_timeline_tweets(self,num_tweets):
        
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline,id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets
            


# In[4]:


#### TWitter Authenticator ####
class TwitterAuthenticator():
    
    def authenticate_twitter_app(self):
        auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
        return auth


# In[5]:


class TwitterStreamer():
    
	"""
	Class for streaming and processing live tweets."""
	def __init__(self):
          self.twitter_authenticator = TwitterAuthenticator()
      

	def stream_tweets(self,fetched_tweets_filename, hash_tag_list):
		# This handles Twitter authentication and the connection to the Twitter Streaming API.
		listener = TwitterListener(fetched_tweets_filename)
		auth  = self.twitter_authenticator.authenticate_twitter_app()
		stream = Stream(auth, listener)
		stream.filter(track = hash_tag_list)


# In[6]:


class TwitterListener(tweepy.StreamListener):
    
    """
    This is a basic listener class that print received tweets
    """
    def __init__(self,fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self,data):
        try:

            print(data)
            with open(self.fetched_tweets_filename,'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data : %s " % str(e))
        return True

    def on_error(self,status):
        if status == 420:
            return False
      
            #Return false on_data method in case rate limit occur
        print(status)


# In[7]:


class TweetAnalyzer():
    """
    Functionality for analyzing and capturing content from tweets.
    """
    
    def clean_tweet(self,tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    
    def analyze_sentiment(self,tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_data_frame(self,tweets):
        df = pd.DataFrame(data = [tweet.text for tweet in tweets], columns = ['Tweets'])
        
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        
        return df
        




def dashboard(request):
    
    #hash_tag_list = ["donald trump","barack obama"]
    #fetched_tweets_filename = "tweets.txt"
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()
    tweets = api.user_timeline(screen_name ="elonmusk",count = 20)
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    print(df.columns)
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['Tweets']])
    print(df.head(10))
 
    # for ind in df.index:
    #     print (df['Tweets'][ind])
    return render(request, 'detection/dashboard.html', {'df' : df})
    #print(dir(tweets[0]))
    #print(tweets[0].retweet_count)
    #print(df.head(10))
    
    # Get average length over all tweets
    #print(np.mean(df['len']))
    
    #Get the number of likes for the most liked tweet
    #print(np.max(df['likes']))
    
    #Get the number of retweets for the most retweeted tweet
    #print(np.max(df['retweets']))
    #### data visualization
    #time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    #time_likes.plot(figsize=(16,4), color='r')
    #plt.show()
    #print(df['date'])
    #time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    #time_retweets.plot(figsize=(16 , 4), color='r')
    #plt.show()