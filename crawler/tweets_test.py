import tweepy
import json
from tweepy import OAuthHandler
import time
from tweepy.streaming import StreamListener

consumer_key = 'ISXRjwy6li8EGINtzqPjVNFdX'
consumer_secret = '11bWe9Zc4OtfM0A2MX4vIhBRUAKvVgd0cPzF9icjykeYLyIICC'
access_token = '1383630322194026500-myiCV4MnRg4K7bEZNjvLlpfJSBFRf0'
access_secret = 'zIrrjOUxug3eioQ3ZigMlltudA58yuRpXdsd0HdWzshfc'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# search_term = "exercise OR diet OR Yoga OR weightlose OR slim OR gym OR calorie OR muscle OR fatburn"
search_term = 'bitcoin'
with open("bitcoin_nsw.json","w") as f:
    # api.search
    count=0
    for tweet in tweepy.Cursor(api.search, q=search_term, geocode = "-32.238539,147.516999,500km", result_type="recent", include_entities=False).items(1000000):
        # print(tweet._json)
        f.write(json.dumps(tweet._json)+"\n")
        count+=1
    f.write("total counts:"+ str(count)+"\n")