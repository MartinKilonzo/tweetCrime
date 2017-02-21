import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from credentials import access_token, access_token_secret, consumer_key, consumer_secret
from userTweets import UserTweets



class TweetListener(StreamListener):

    def __init__(self, fileStream, tweetFields, userList=None, tweetTarget=float('inf')):
        self.fileStream = fileStream
        self.tweetFields = tweetFields
        self.userList = userList
        self.bytesWritten = float(0)
        self.numTweets = 0
        self.tweetTarget = tweetTarget


    def _writeTweet(self, tweet, fileStream=None):
        if fileStream is None:
            fileStream = self.fileStream

        json.dump(tweet, fileStream)
        fileStream.write('\n')
        self.bytesWritten += len(tweet)
        self.numTweets += 1


    def on_data(self, data):
        # If the filestream was not initialized, print to stdout
        if self.fileStream == None:
            print '[TweetStream] {:s}'.format(str(data))
            return True

        # If the target number of tweets has not been reached, continue to collect tweets
        elif self.numTweets < self.tweetTarget:
            data = json.loads(data)
            tweet = {}

            # Filter for the required fields
            for field in self.tweetFields:
                tweet[field] = data[field]

            self._writeTweet(tweet)

            user = tweet['user']['screen_name']
            userTweets = []
            # If this user's tweets have not already been fetched
            if user not in self.userList:
                # Add the user to the user list
                self.userList.append(user)

                # Get the user's tweets
                with open('./tweets/userTweets.json', 'a') as userTweetFileStream:
                    userTweets = UserTweets(user).getTweets(True)
                    for tweet in userTweets:
                        self._writeTweet(tweet, userTweetFileStream)

                # Save the user as beeing processed
                with open('./tweets/users.json', 'a') as userFileStream:
                    json.dump(user, userFileStream)
                    userFileStream.write('\n')

            self.bytesWritten += len(str(tweet)) * len(userTweets)
            print '[TweetStream] Wrote {:d} tweets comprising {:.2f} megabytes to file.'.format(self.numTweets, self.bytesWritten/1024/1024)
            return True

        # If the target tweets has been reached, close off the JSON array, and end the stream
        else:
            self.fileStream.close()
            print '[TweetStream] Finished. Wrote {:d} tweets comprising {:.2f} megabytes to file.'.format(self.numTweets, self.bytesWritten/1024/1024)
            return False


    def on_error(self, status):
        print '[TweetStream] {:s}'.format(str(status))
        if status == 420:
            self.fileStream.close()
            return False



if __name__ == '__main__':

    with open('./tweets/Template.json', 'r') as fs:
        tweetKeys = json.load(fs).keys()

    ul = []
    with open('./tweets/users.json', 'r') as fs:
        for line in fs:
            ul.append(json.loads(line))

    print '[TweetStream] User List: {:s}'.format(str(ul))

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    with open('./tweets/vanTweets2.json', 'a') as fs:
        listener = TweetListener(fs, tweetKeys, ul)
        stream = Stream(auth, listener)
        stream.filter(locations=[-123.22474, 49.198177, -123.023068, 49.317294])
