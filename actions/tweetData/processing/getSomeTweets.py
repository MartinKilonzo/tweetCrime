import sys
import getopt
from datetime import date, datetime, time, timedelta
import json


def getTweetsFor(days):
    endDate = -1
    tweets = []
    with open('./tweets/vanTweets.json', 'r') as fileStream:
        # Iterates through the file line by line
        for line in fileStream:
            data = json.loads(line)
            tweetDate = int(data['timestamp_ms']) / 1000

            if endDate == -1:
                startDate = datetime.fromtimestamp(tweetDate).date()
                endDate = startDate + timedelta(days=days)
                endDate = (datetime.combine(endDate, datetime.min.time()
                                            ) - datetime(1970, 1, 1)).total_seconds()
                endDate = int(endDate)

            if tweetDate < endDate:
                entities = data['entities']
                symbols = None
                hashtags = None
                user_mentions = None
                urls = None
                if len(entities['hashtags']) > 0:
                    hashtags = entities['hashtags']
                if len(entities['symbols']) > 0:
                    symbols = entities['symbols']
                if len(entities['user_mentions']) > 0:
                    user_mentions = entities['user_mentions']
                if len(entities['urls']) > 0:
                    urls = entities['urls']

                tweet = {
                    'lang': data['lang'],
                    'text': data['text'],
                    'symbols': symbols,
                    'hashtags': hashtags,
                    'user_mentions': user_mentions,
                    'urls': urls,
                    'coordinates': data['coordinates'],
                    'timestamp_ms': data['timestamp_ms'],
                    'is_quote_status': data['is_quote_status'],
                    'id_str': data['id_str'],
                    'is_reply': data['in_reply_to_user_id'] != None,
                    'retweet_count': data['retweet_count'],
                    'favorite_count': data['favorite_count'],
                    'source': data['source'],
                }
                tweets.append(tweet)

    return tweets


def fetchTweets(args):
    """
    MAIN
    """
    # Get Room
    days = 0
    try:
        opts, args = getopt.getopt(args, 'hd:', ['days='])
    except getopt.GetoptError:
        print 'Usage: $ python getSomeTweets.py -d <num_days_from_start>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: $ python getSomeTweets.py -d <num_days_from_start>'
        elif opt in ('-d', '--days'):
            arg = int(float(arg))
            days = arg

    return getTweetsFor(days)


if __name__ == '__main__':
    # tweetList = fetchTweets(sys.argv[1:])
    tweetList = getTweetsFor(7)
    # test = tweetList[0]['timestamp_ms']
    print len(tweetList)
    tweetList[0]

    count = 0
    for tweet in tweetList:
        print tweet

    print count
    print count / len(tweetList)

    with open('singleTweet.json', 'w') as fileStream:
        json.dump(tweetList[0], fileStream)


# Checkout JQ for filtering JSON
