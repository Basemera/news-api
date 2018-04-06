from flask import make_response, jsonify

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
