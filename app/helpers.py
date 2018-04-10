from flask import make_response, jsonify
from string import punctuation

def get_topics_response(topics, status_code):
    return make_response(jsonify({
            'topics':topics,
            'status':'success'
        }
    )), status_code

def get_articles_response(articles, status_code, status):
    return make_response(jsonify({
        'articles':articles,
        'status': status
    })), status_code

def get_articles_by_date_response(articles, status_code, status):
    return make_response(jsonify({
        'articles':articles,
        'status':status,
    })), status_code

def response(status,message, status_code):
    return make_response(jsonify({
        'status': status,
        'message': message
    })), status_code

def generate_article_url(title):
    
    split_title = title.translate(str.maketrans("","", punctuation)).split( )
    article_url = "-".join(split_title)
    return article_url
