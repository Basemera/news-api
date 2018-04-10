import json
from flask import jsonify, request
from dateutil.parser import parse
from app import app
from .punch import Punch
from .helpers import get_topics_response, get_articles_response, response, get_articles_by_date_response

punch = Punch()

@app.route('/topics', methods=['GET'])
def get_topics():
    return get_topics_response(punch.get_topics(), 200)

@app.route('/articles/', methods=['GET'])
def get_articles():
    """
    Get all the articles from Punch
    """
    topic = request.args.get('topic').lower()
    date_provided = request.args.get('date')
    try:
        str(topic)
        if date_provided:
            parse(date_provided).timestamp()
    except ValueError:
        return response('failed', 'Provide a valid topic or date', 400)
    if topic in punch.get_topics():
        if date_provided:
            date = parse(date_provided).timestamp()
            return get_articles_by_date_response(punch.get_articles_by_date(topic, date), 200, 'success')
        return get_articles_response(punch.get_articles(topic), 200, 'success')

@app.route('/articleContent', methods=['GET'])
def get_article_content():
    return

