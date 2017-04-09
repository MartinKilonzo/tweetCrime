import json


test = {"lang": "en", "retweet_count": 33}

test.keys()
test1 = {"lang": "fr", "retweet_count": 0, "palace": False}

def getKeyPath(template, object):
    if type(object) is not 'dict':
        return path

    print 'process'
    for key in object.keys():
        getKeyPath(object[key])
