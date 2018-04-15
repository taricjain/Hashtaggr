import json
import requests
import time
import hashlib
import string
import random
import os
from flask import Flask, request, Response
from flask_cors import CORS
from requests_oauthlib import OAuth1
from newsapi import NewsApiClient
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
from classify import get_sentiments

app = Flask(__name__)
CORS(app)
# News api class object
newsapi = NewsApiClient(api_key='52b9002043834474907063ae1d72519f')
blob = Blobber(analyzer=NaiveBayesAnalyzer())



TWITTER_CONSUMER_KEY = "UVvvyBVaG2OLZSZcc5qeIvdR9"
TWITTER_COMSUMER_SECRET = "lVw6ubIxHyqwkynJpqkDYAhNT4vuDPAPEVYLXDDkq3dfUilb6i"
TWITTER_ACCESS_TOKEN = "1421480659-uk05gUqnbJK7bAiWyh4uSU9bOD6mBxXQIpbYsAj"
TWITTER_ACCESS_SECRET = "1r7ry7s63tjgZZRNnUfmhYzRGaQJL2rUDjU2VTV4KW69o"

@app.route('/', methods=['GET'])
def index_route():
    return 'server'

@app.route('/oauth/instagram/')
def instagram_oauth_handler():
    instagram_code = request.args.get('code') #getting code from url
    output = "Code: {}".format(instagram_code)
    params = {
            'client_id': '9e25b8547bc14635b3a883f88048362f',
            'client_secret': 'c454fe6508524a799ace16eacd7c689c',
            'grant_type': 'authorization_code',
            'redirect_uri': 'http://localhost:8000/oauth/instagram/access_token',
            'code': instagram_code
    } # request payload needed to get access_toke from instagram
    r = requests.post('http://api.instagram.com/oauth/access_token', data=params)
    response = json.loads(r.content)
    output = "\nAccess Token: {}".format(response['access_token'])
    return output

@app.route('/data/twitter/')
def get_twitter_data():
    url = "https://api.twitter.com/1.1/search/tweets.json"

    querystring = {"q": request.args.get("query", ""), "lang": "en", "count": 100}
    auth = OAuth1(
        TWITTER_CONSUMER_KEY, TWITTER_COMSUMER_SECRET,
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
    response = requests.get(url, auth=auth, params=querystring)
    return json.dumps(twitter_parser(json.loads(response.text)))

@app.route('/data/instagram/')
def get_instagram_data():
    search_tag = request.args.get("query").split(' ')
    search_tag = ''.join(search_tag)
    url = "https://www.instagram.com/explore/tags/{}/?__a=1".format(search_tag)

    instagram_response = requests.get(url)

    # Generate a token 
    # Save json data to file
    # Save file

    instagram_response = json.loads(instagram_response.text)
    token = rnd_string_hash()
    data_file = "{}.json".format(token)

    write_to_file(data_file, json.dumps(instagram_response))

    return return_response(token, instagram_parser(instagram_response))

@app.route('/data/news/')
def get_news_data():
    search_query = str(request.args.get("query"))
    top_headlines = newsapi.get_top_headlines(q=search_query, language='en')
    # Generate a token 
    # Save json data to file
    # Save file
    token = rnd_string_hash()
    data = json.dumps(top_headlines)
    data_file = "{}.json".format(token)
    
    write_to_file(data_file, data) # returns nothing

    return return_response(token, top_headlines)


@app.route('/data/sentiments/news/')
def get_news_sentiment():
    filename = "{}.json".format(request.args.get("token"))
    response_sentiment = {
        'positive': 0.0,
        'negative': 0.0
    }
    response_counter = {
        'positive': 0,
        'negative': 0
    }
    # get data from file
    data = read_from_file(filename)
    for article in data["articles"]:
        sentiment = get_sentiments(article["title"].encode("utf-8"), blob)
        response_sentiment[sentiment['sentiment']] += sentiment['percent']
        response_counter[sentiment['sentiment']] += 1

    response_sentiment['positive'] = float(response_sentiment['positive'] / response_counter['positive'])

    response_sentiment['negative'] = 100 - response_sentiment['positive']
    #return data
    os.remove(filename)
    return json.dumps(response_sentiment)



@app.route('/data/setiments/social/')
def get_social_setiment():
    filename = "{}.json".format(request.args.get("token"))
    # pass to classifier
    # get an average
    # return
    return filename




# ################################# PARSERS ######################################


def return_response(token, data):
    resp = Response(json.dumps({'token': token, 'data': data}))
    resp.headers['Content-Type'] = "application/json"
    return resp

def twitter_parser(data):
    parsed_tweets = list()
    for tweet in data["statuses"]:
        temp_tweet = {
            'text': tweet['text'],
            'url': 'https://twitter.com/statuses/{}'.format(tweet['id_str'])
        }
        parsed_tweets.append(temp_tweet)
    return parsed_tweets
    

def instagram_parser(data):
    parsed_insta_posts = list()
    for post in data["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]:
        temp_post = {
            'text': post["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"],
            'display_url': post["node"]["display_url"]
        }
        parsed_insta_posts.append(temp_post)
    return parsed_insta_posts

def write_to_file(data_file, data):
    fhandle = open(data_file, 'w')
    fhandle.write(data)
    fhandle.close()

def read_from_file(data_file):
    fhandle = open(data_file, 'r')
    data = fhandle.read()
    fhandle.close()
    return json.loads(data)

def rnd_string_hash(length=10):
    rnd_str = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
    return hashlib.sha256(rnd_str).hexdigest()

if __name__ == "__main__":
    app.run(debug=True, port=8000)
