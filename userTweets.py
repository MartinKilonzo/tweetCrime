import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream

from credentials import access_token, access_token_secret, consumer_key, consumer_secret



class UserTweets():


    def __init__(self, screenName):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = API(auth)
        self.screenName = screenName


    def getTweets(self, verbose=False):
        # This method will return the most recent 3240 tweets from the user
        tweets = []
        lastTweet = None
        newTweets = self.api.user_timeline(screen_name=self.screenName, count=200, max_id=lastTweet)
        while len(newTweets) > 0:
            lastTweet = newTweets[-1].id - 1
            tweets.extend([tweet._json for tweet in newTweets])
            newTweets = self.api.user_timeline(screen_name=self.screenName, count=200, max_id=lastTweet)
        if verbose:
            print '[UserTweets] Added {:d} tweets from {:s}.'.format(len(tweets), self.screenName)

        return tweets



if __name__ == '__main__':

    user = 'realDonaldTrump'
    tweetList = UserTweets(access_token, access_token_secret, consumer_key, consumer_secret)

    with open(user + 'Tweets.json', 'w') as fileStream:
        json.dump(tweetList.getTweetsFromUser(user), fileStream, indent = 4)


    with open(user + 'Tweets.json', 'r') as fileStream:
        data = json.load(fileStream)

    userData = []
    for tweet in data:
        t = {
        'id_str': tweet['id_str'],
        'text': tweet['text'],
        'coordinates': tweet['coordinates'],
        'created_at': tweet['created_at'],
        'entities': tweet['entities'],
        'geo': tweet['geo'],
        'in_reply_to_user_id_str': tweet['in_reply_to_user_id_str'],
        'favorite_count': tweet['favorite_count'],
        'location': tweet['location'],
        'retweet_count': tweet['retweet_count'],
        }
        userData.append(t)

    with open(user + 'Data.json', 'w') as fileStream:
        json.dump(userData, fileStream, indent = 4)
