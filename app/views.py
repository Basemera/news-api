import json
from flask import jsonify, request
from dateutil.parser import parse
from app import app
from .punch import Punch
from .helpers import get_topics_response, get_articles_response, get_articles_by_date, response

punch = Punch()

@app.route('/topics', methods=['GET'])
def get_topics():
    return get_topics_response(punch.getTopics(), 200)

@app.route('/articles/', methods=['GET'])
def get_articles():
    topic = request.args.get('topic').lower()
    date_provided = request.args.get('date')
    try:
        str(topic)
        if date_provided:
            parse(date_provided).timestamp()
    except ValueError:
        return response('failed', 'Provide a valid topic or date', 400)
    if topic in punch.getTopics():
        if date_provided:
            return get_articles_by_date(punch.get_articles_by_date(topic, parse(date_provided).timestamp()), 'success', 200)
        return get_articles_response(punch.getArticles(topic), 200, 'success')

