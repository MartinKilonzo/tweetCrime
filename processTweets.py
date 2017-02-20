import json


list = []
with open('./tweets/vanTweets.json', 'r') as fileStream:
    for line in fileStream:
        list.append(json.loads(line))

list
