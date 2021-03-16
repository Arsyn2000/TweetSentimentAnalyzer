import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):
    # A generic class for sentiment analysis
    # Constructor of the class TwitterClient
    def __init__(self):
        # Making variables and assigning them the value of keys from Twitter for developers
        consumer_key = 'tS1Ce5h0QEvjJbqJ2xP6hOoYE'
        consumer_secret = 'Gbj46JEbRorlJikXGp8SBP5LdjxXKd3YI7v9ZK6kq8VX7mcoA7'
        access_token = '841562725-lzjnOSKHnMXUIYFCmo0SG5labRVNvUrZhAWK148p'
        access_token_secret = 'ebRWTRi1AEGu6qCB31bO6WF9582Qr1zTXAJCT06sy4Q80'

        # Trying to authenticate
        try:
            # Creating OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # Setting access_token of the object created
            self.auth.set_access_token(access_token, access_token_secret)
            # Creating API to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error : Authentication Failed")

    def clean_tweet(self, tweet):
        # Method is Used to remove links, special characters, from the tweet using regular expression statements
        # The re.sub() method performs global search and global replace on the given string.
        # It is used for substituting a specific pattern in the string.
        # Syntax: re.sub(pattern, repl, string, count=0, flags=0)
        # pattern – the pattern which is to be searched and substituted
        # repl - the string with which the pattern is to be replaced
        # string - tha name of the variable in which the pattern is stored
        # count - number of characters upto which substitution will be performed
        # flags - it is used to modify the meaning of regex pattern
        # count and flags are optional arguments
        rex = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet)
        # print(rex)
        return ' '.join(rex.split())

    def get_tweet_sentiment(self, tweet):
        # A utility function to classify the sentiment of the passed tweet using textblob's sentiment method
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=100):
        # An empty list to store the parsed tweets
        tweets = []
        try:
            # Call Twitter API to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)
            # Parsing tweets
            for tweet in fetched_tweets:
                # Empty dictionary to store required parameters of a tweet
                parsed_tweet = {'text': tweet.text, 'sentiment': self.get_tweet_sentiment(tweet.text)}

                # Checking for retweets
                # If a tweet has retweets append it only once
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            return tweets
        except tweepy.TweepError as e:
            print("Error : " + str(e))
