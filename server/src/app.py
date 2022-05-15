from flask import Flask, jsonify
from flask_restful import Api
import os
import socket
import requests
import json
# from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords

app = Flask(__name__)
# my api key to apidiscounts
api_key = 'EaDeMioN'
api = Api(app)

nltk.download('stopwords')

set(stopwords.words('english'))


# flask routes totorial reference
# https://www.youtube.com/watch?v=SdTzwYmsgoU

# function to fetch hostname and ip
@app.route('/')
def fetchDetails():
    # basic route that returns your hostname and ip address when called
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    return str(host_name), str(host_ip)


@app.route('/deals/<query>', methods=['GET', 'POST'])
def get_deals(query):
    # Call api.discountapi to get deals based on a search query
    url = f"https://api.discountapi.com/v2/deals?query={query}"  
    req = requests.get(url)
    data = json.loads(req.content)
    # Loop through deals and append each deal to a list to return
    newList = []
    for i in data['deals']:
        newList.append(i['deal'])
        # print(i['deal']['title'])
    return json.dumps(newList)


@app.route('/sentiment/<query>', methods=['POST', 'GET'])
def my_form_post(query):
    # getting stop words for the english language
    stop_words = stopwords.words('english')
    # appending each word from the query into a final string
    text_final = ''.join(c for c in query if not c.isdigit())
   
    # joining all the words in text final and stripping out the stop words that have no relevance to the sentiment
    processed_doc1 = ' '.join([word for word in text_final.split() if word not in stop_words])

    # declare a sentiment analyzer object from vader sentiment package.
    sa = SentimentIntensityAnalyzer()
    dd = sa.polarity_scores(text=processed_doc1)
    print(dd)
    compound = round((1 + dd['compound'])/2, 2)
    print(compound)
    dd['compound'] = compound
    # return sentiment scores in json format
    return json.dumps(dd)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))