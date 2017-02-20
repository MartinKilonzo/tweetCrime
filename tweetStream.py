import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from credentials import access_token, access_token_secret, consumer_key, consumer_secret



class TweetListener(StreamListener):

    def __init__(self, fileStream, tweetFields, tweetTarget=float('inf')):
        self.fileStream = fileStream
        self.tweetFields = tweetFields
        self.bytesWritten = float(0)
        self.numTweets = 0
        self.tweetTarget = tweetTarget


    def on_data(self, data):
        # If the filestream was not initialized, print to stdout
        if self.fileStream == None:
            print data
            return True

        # If the target number of tweets has not been reached, continue to collect tweets
        elif self.numTweets < self.tweetTarget:
            data = json.loads(data)
            tweet = {}

            # Filter for the required fields
            for field in self.tweetFields:
                tweet[field] = data[field]

            json.dump(tweet, self.fileStream)
            self.fileStream.write('\n')

            self.bytesWritten += len(str(tweet))
            self.numTweets += 1
            if self.numTweets % 10 == 0:
                print 'Wrote {:d} tweets comprising {:.2f} megabytes to file.'.format(self.numTweets, self.bytesWritten/1024/1024)
            return True

        # If the target tweets has been reached, close off the JSON array, and end the stream
        else:
            self.fileStream.close()
            print 'Finished. Wrote {:d} tweets comprising {:.2f} megabytes to file.'.format(self.numTweets, self.bytesWritten/1024/1024)
            return False


    def on_error(self, status):
        print status
        if status == 420:
            self.fileStream.close()
            return False



if __name__ == '__main__':

    with open('./tweets/Template.json') as fs:
        tweetKeys = json.load(fs).keys()

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    with open('./tweets/vanTweets.json', 'a') as fs:
        listener = TweetListener(fs, tweetKeys)
        stream = Stream(auth, listener)
        stream.filter(locations=[-123.22474, 49.198177, -123.023068, 49.317294])
