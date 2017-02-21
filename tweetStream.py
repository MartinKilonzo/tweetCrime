import os
import json
from datetime import datetime

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from credentials import access_token, access_token_secret, consumer_key, consumer_secret
from userTweets import UserTweets



def log(message):
    with open('streamlog.txt', 'a') as logStream:
        print '[TweetStream] {:s}'.format(message)
        logStream.write('[{:s}] {:s}\n'.format(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), message))



class TweetListener(StreamListener):



    def __init__(self, fileStream, tweetFields, location, userList=None, tweetTarget=float('inf')):
        self.fileStream = fileStream
        self.tweetFields = tweetFields
        self.bounds = location
        self.userList = userList
        self.bytesWritten = float(0)
        self.numTweets = 0
        self.tweetTarget = tweetTarget
        log('Starting Stream...')



    def __writeTweet(self, data, fileStream=None):
        # Filter for the required fields
        tweet = {}
        for field in self.tweetFields:
            try:
                tweet[field] = data[field]
            except KeyError: pass

        if fileStream is None:
            fileStream = self.fileStream

        json.dump(tweet, fileStream)
        fileStream.write('\n')
        self.bytesWritten += len(str(tweet))
        self.numTweets += 1



    def __tweetInBounds(self, tweet):
        location = tweet['coordinates']
        if location is None:
            return False
        location = location['coordinates']
        long1, lat1, long2, lat2 = self.bounds
        return location[0] > long1 and location[0] < long2 and location[1] > lat1 and location[1] < lat2



    def __getUserTweets(self, user):
        userTweets = []
        # If this user's tweets have not already been fetched
        if user not in self.userList:
            # Add the user to the user list
            self.userList.append(user)

            # Get the user's tweets
            with open('./tweets/userTweets.json', 'a') as userTweetFileStream:
                userTweets = UserTweets(user).getTweets(True)
                for tweet in userTweets:
                    if self.__tweetInBounds(tweet):
                        self.__writeTweet(tweet, userTweetFileStream)

            # Save the user as beeing processed
            with open('./tweets/users.json', 'a') as userFileStream:
                json.dump(user, userFileStream)
                userFileStream.write('\n')



    def on_data(self, data):
        lastNumTweets = self.numTweets
        lastSizeTweets = self.bytesWritten
        # If the filestream was not initialized, print to stdout
        if self.fileStream == None:
            log('{:s}'.format(str(data)))
            return True

        # If the target number of tweets has not been reached, continue to collect tweets
        elif self.numTweets < self.tweetTarget:
            tweet = json.loads(data)
            # Save the current tweet
            self.__writeTweet(tweet)
            # Get the user's past tweets
            user = tweet['user']['screen_name']
            self.__getUserTweets(user)

            log('Wrote {:d} tweets as {:.2f} MB to file. Total: {:d} tweets as {:.2f} MB.'.format(self.numTweets - lastNumTweets, (self.bytesWritten - lastSizeTweets)/1024/1024, self.numTweets, self.bytesWritten/1024/1024))
            return True

        # If the target tweets has been reached, close off the JSON array, and end the stream
        else:
            self.fileStream.close()
            log('Finished. Wrote {:d} tweets as {:.2f} MB to file.'.format(self.numTweets, self.bytesWritten/1024/1024))
            return False



    def on_error(self, status):
        log('{:s}'.format(str(status)))
        if status == 420:
            self.fileStream.close()
            return False



if __name__ == '__main__':

    VANCOUVER_BOUNDS = [-123.224215, 49.19854, -123.022947, 49.316738]
    with open('./Template.json', 'r') as fs:
        tweetKeys = json.load(fs).keys()


    userPath = './tweets/users.json'
    if not os.path.isfile(userPath):
        open(userPath, 'a').close()
    ul = []
    with open(userPath, 'r') as fs:
        for line in fs:
            ul.append(json.loads(line))

    print 'User List: {:s}'.format(str(ul))

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    with open('./tweets/vanTweets.json', 'a') as fs:
        listener = TweetListener(fs, tweetKeys, VANCOUVER_BOUNDS, ul)
        stream = Stream(auth, listener)
        stream.filter(locations=VANCOUVER_BOUNDS)
