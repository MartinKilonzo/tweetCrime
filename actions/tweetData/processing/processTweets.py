import json


list = []
with open('./tweets/userTweets.json', 'r') as fileStream:
    for line in fileStream:
        list.append(json.loads(line))

VANCOUVER_BOUNDS = [-123.224215, 49.19854, -123.022947, 49.316738]


def tweetInBounds(tweet):
    location = tweet['coordinates']
    if location is None:
        return False
    location = location['coordinates']
    long1, lat1, long2, lat2 = VANCOUVER_BOUNDS
    flag = location[0] > long1 and location[0] < long2 and location[1] > lat1 and location[1] < lat2
    city = tweet['place']['name']
    print '{:5s} {:s} {:s}'.format(str(flag), location, city)


for tweet in list:
    tweetInBounds(tweet)
