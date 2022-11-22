import tweepy
import os
import random
from time import sleep


CONSUMER_KEY='O2se0zpXDNsozClRlCrXfV1ZK'
CONSUMER_SECRET='cDjPlrXgFSIGF9RfWUsf0bCWWsa5QuxhGvOzmaUoDClNrKrlmL'
ACCESS_TOKEN='ACCESS_TOKEN'
ACCESS_TOKEN_SECRET='ACCESS_TOKEN_SECRET'
WAIT_TIME_HOURS = 0.5
TWEETS = []

# function to authorize bot account
def authorize_twitter_application(consumer_key, consumer_secret):
    #based on: https://developer.twitter.com/en/docs/authentication/oauth-1-0a/pin-based-oauth
    '''
        Authorize twitter application to perform task on behalf of user.
        Returns access_token and access_token_secret
    '''
    #consumer_key='O2se0zpXDNsozClRlCrXfV1ZK'
    #consumer_secret='cDjPlrXgFSIGF9RfWUsf0bCWWsa5QuxhGvOzmaUoDClNrKrlmL'
    #credit on twitter bot: https://twittercommunity.com/t/multiple-bot-accounts/128332
    #credit: https://gist.github.com/hezhao/4772180#gistcomment-2583970 , https://gist.github.com/hezhao/4772180#gistcomment-3213988
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback='oob')
    # get access token from the user and redirect to auth URL
    auth_url = auth.get_authorization_url()
    print('Visit this authorization URL from your browser: ' + auth_url)

    # ask user to verify the PIN generated in broswer
    verifier = input('PIN: ').strip()
    auth.get_access_token(verifier)
    print('ACCESS_KEY = "{}"'.format(auth.access_token))
    print('ACCESS_SECRET = "{}"'.format(auth.access_token_secret))
    
    client = tweepy.Client(consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=auth.access_token,
    access_token_secret=auth.access_token_secret)
    return client

# function for first "Hello, World!" tweet from the guide
def post_first_tweet():
    client = tweepy.Client(consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET)


    response = client.create_tweet(text='Hello, World!')
    print(response)

# function to generate tweet from .txt file containing possible tweets
def get_tweet_text(header_file, body_file):
    tweet_invalid = True
    while tweet_invalid:
        try:
            with open(header_file, 'r') as f:
                tweet_headers = f.read().splitlines()
            randomly_picked_header = tweet_headers[random.randrange(len(tweet_headers))]
        
            with open(body_file, 'r') as f:
                tweets = f.read().splitlines()
            randomly_picked_tweet = tweets[random.randrange(len(tweets))]
        
            final_tweet = '{}\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n{}'.format(randomly_picked_header, randomly_picked_tweet)
            if (len(final_tweet)>280 or final_tweet in TWEETS):
                tweet_invalid = True
            else:
                tweet_invalid = False
                TWEETS.append(final_tweet)
        except Exception as e:
            print(e)
    print(final_tweet)
    return final_tweet
    
# function to post tweet every 30 min
def tweet_text():
    client = authorize_twitter_application(CONSUMER_KEY, CONSUMER_SECRET)
    while True:
        try:
            tweet = get_tweet_text('/Users/sofiahuang/Desktop/TwitterHeading.txt', '/Users/sofiahuang/Desktop/TwitterBody.txt')
            response = client.create_tweet(text=tweet)
        except tweepy.TweepError as e:
            print(e.reason)
        sleep(60*60*WAIT_TIME_HOURS)

if __name__ == "__main__":
    #authorize_twitter_application(CONSUMER_KEY, CONSUMER_SECRET)
    #post_first_tweet()
    #get_tweet_text('/Users/sofiahuang/Desktop/TwitterHeading.txt', '/Users/sofiahuang/Desktop/TwitterBody.txt')
    tweet_text()