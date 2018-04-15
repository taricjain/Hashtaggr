from textblob import TextBlob
import re

def classify(string, blob):
    data = dict()
    data['orig'] = string
    data['clean'] = clean_string(string)
    blobber = blob(data['clean'])
    data['positive'] = float(blobber.sentiment.p_pos)
    data['negative'] = float(blobber.sentiment.p_neg)

    if data['positive'] > data['negative']:
        data['sentiment'] = 'positive'
        data['percent'] = data['positive'] * 100
    elif data['negative'] > data['positive']:
        data['sentiment'] = 'negative'
        data['percent'] = data['negative'] * 100
    else:
        data['sentiment'] = 'neutral'
        data['percent'] = 0
    return data

def clean_string(string):
    remove_url = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', string)
    remove_hastag = re.sub('#', '', remove_url)
    cleaned = re.sub('\'', '', remove_hastag)
    return cleaned

def get_sentiments(string, blob):
	return classify(string.decode('utf-8'), blob)
