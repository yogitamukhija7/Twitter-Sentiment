import re
import os
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import Analysis.combine
from django.conf import settings
 
class TwitterClient(object):
    '''Twitter class for senti analysis.'''
    def __init__(self):
        consumer_key = settings.CONSUMER_KEY
        consumer_secret = settings.CONSUMER_SECRET
        access_token = settings.ACCESS_TOKEN
        access_token_secret = settings.ACCESS_TOKEN_SECRET
 
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication failed")
 
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))    
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query, count = 50):
        tweets = []
 
        try:
            fetched_tweets = self.api.search(q = query, count = count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
                parsed_tweet['text'] = tweet.text.translate(non_bmp_map)
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
class TwitterObject(object):
    def __init__(self):
        self.api=TwitterClient()
        self.subj='';
        self.ptweets=[]
        self.tweets=[]
        self.ntweets=[]
        self.neutral=[]

    def fetchTweets(self):
        self.tweets = self.api.get_tweets(self.subj, count = 200)
        p1=os.path.join(settings.BASE_DIR,"sentiment","Analysis","dataset","example_tweets.txt")
        p2=os.path.join(settings.BASE_DIR,"sentiment","Analysis","dataset","testingTokenised.txt")
        p3=os.path.join(settings.BASE_DIR,"sentiment","Analysis","ark-tweet-nlp","runTagger.sh")
        os.system(p3+" "+ p1 + " > " + p2) 
        
        # self.ptweets = [tweet for tweet in self.tweets if tweet['sentiment'] == 'positive']
        # self.ntweets = [tweet for tweet in self.tweets if tweet['sentiment'] == 'negative']
        # self.neutral=[tweet for tweet in self.tweets if tweet['sentiment']=='neutral']


obj = TwitterObject()
obj.fetchTweets()