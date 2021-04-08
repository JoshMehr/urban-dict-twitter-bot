import json
import twitter
from urbandict import *
import requests
import random
import html
from blacklisted import nonowords
from signin import *

a_token = atoken
a_token_secret = atoken_secret
c_key = ckey
c_secret = csecret


def getWord():
    rand = (str)(random.randint(1, 2222))

    url = "https://www.urbandictionary.com/random.php?page=" + rand
    r = requests.get(url)
    print(rand)
    word = r.text
    word = word[word.find('class="word"'):]
    word = word[word.find('">') + 2:word.find('</')]
    word = html.unescape(word)
    print(word)
    # print(url, s, "\n",r.text)
    return word


def defi(s):
    stuff = []
    try:
        stuff.append(s)
        stuff.append(define(s).__getitem__(0).get('def'))
        stuff.append(define(s).__getitem__(0).get('example'))

    except:
        s = getWord()
        stuff = defi(s)
    return stuff

def lambda_handler(event, context):
    api = twitter.Api(consumer_key=c_key, consumer_secret=c_secret, access_token_key=a_token,access_token_secret=a_token_secret)

    s = getWord()
    dict = defi(s)
    werd = dict.__getitem__(0)
    definition = dict.__getitem__(1)
    example = dict.__getitem__(2)

    # print(s + ": " + definition + "\n" + example)

    tweet = [werd + ":\n" + definition, "Example:\n" + example]
    x = 0
    while x == 0:
        offensive = 0
        for bword in nonowords:
            if bword in tweet[0].lower() or bword in tweet[1].lower():
                offensive += 1
        
        if len(tweet[0]) <= 280 and len(tweet[1]) <= 280 and offensive == 0:
            statu = api.PostUpdate(status=tweet[0])
            print(tweet[0])
            x += 1
        else:
            s = getWord()
            dict = defi(s)
            werd = dict.__getitem__(0)
            definition = dict.__getitem__(1)
            example = dict.__getitem__(2)
            tweet = [werd + ":\n" + definition, "Example:\n" + example]
    api.PostUpdate(status=tweet[1], media=None, media_additional_owners=None, media_category=None,in_reply_to_status_id=statu.id)
    print(tweet[1])

    return {
        "statusCode": 200,
        "body": json.dumps('Hello from Lambda!')
    }
