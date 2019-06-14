from flask import Flask
from sentiment_analyzer import *
import requests
import json

app = Flask(__name__)

@app.route('/hello_world')
def hello_world():
    return 'Hello, World!'

@app.route('/hello_tobin')
def hello_tobin():
	return 'Hello Tobin'

@app.route('/hacker_news_top_50_titles')
def obtain_top_50_titles():

	response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
	top_50_ids = response.json()[:50]
	print(top_50_ids)

	titles = []
	for x in top_50_ids:
		current_top_story_api_url = 'https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'.format(x)
		current_top_story = requests.get(current_top_story_api_url).json()
		current_top_title =  current_top_story['title']
		titles.append(current_top_title)

	return json.dumps(titles)

@app.route('/top_5_comments')
def obtain_top_5_comments():
	response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
	top_10_ids = response.json()[:10]

	comments = {}

	for x in top_10_ids:
		current_top_story_api_url = 'https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'.format(x)
		current_top_story = requests.get(current_top_story_api_url).json()
		current_top_title =  current_top_story['title']
		current_top_comments_ids =  current_top_story['kids'][:5]

		current_comments = {}

		for y in current_top_comments_ids:
			current_top_comments_api_url = ' https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'.format(y)
			current_top_comment = requests.get(current_top_comments_api_url).json()
			if 'text' in current_top_comment:
				counts = sentiment_analysis(current_top_comment['text'])
				current_comments[current_top_comment['by']] = counts

		comments[current_top_title] = current_comments

	return json.dumps(comments)

if __name__ == "__main__":
	app.run()