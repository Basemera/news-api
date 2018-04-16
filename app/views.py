from flask import jsonify, request
from dateutil.parser import parse
from app import app
from app.punch import Punch
from app.helpers import get_topics_response, get_articles_response, value_error_response, get_articles_by_date_response

punch = Punch()


@app.route('/topics', methods=['GET'])
def get_topics():
    """
        Get all the topics from Punch
    """

    return get_topics_response(punch.get_topics(), 200)


@app.route('/articles/', methods=['GET'])
def get_articles():
    """
    Get all the articles from Punch
    """
    topic_caps = request.args.get('topic')
    date_provided = request.args.get('date')
    page = request.args.get('page', 1)

    if not page.isdigit():
        return value_error_response('failure', 'Page must be an interger', 400)
    if not topic_caps:
        return value_error_response('failure', 'Topic not provided please provide one', 400)
    topic = topic_caps.lower()

    try:
        str(topic)
        if topic not in punch.get_topics():
            return value_error_response('failure', 'No articles for that topic', 400)
        if date_provided:
            parse(date_provided).timestamp()
    except ValueError:
        return value_error_response('failed', 'Provide a valid topic or date', 400)
    if topic in punch.get_topics():
        if date_provided:
            date = parse(date_provided).timestamp()
            return get_articles_by_date_response(punch.get_articles_by_date(topic, page, date), 200, 'success')
        return get_articles_response(punch.get_article(topic, page), 200, 'success')
    return value_error_response('failure', 'No articles for that topic', 400)
