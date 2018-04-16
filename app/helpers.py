from flask import make_response, jsonify
from string import punctuation
import requests
from bs4 import BeautifulSoup


def get_topics_response(topics, status_code):
    """This function makes a response for returning all topics"""
    return make_response(jsonify({
        'topics': topics,
        'status': 'success'
    }
    )), status_code


def get_articles_response(articles, status_code, status):
    """This function makes a response for returning all the details of an article"""
    return make_response(jsonify({
        'articles': articles,
        'status': status
    })), status_code


def get_articles_by_date_response(articles, status_code, status):
    """This function makes a response for returning all articles by date"""
    return make_response(jsonify({
        'articles': articles,
        'status': status,
    })), status_code


def value_error_response(status, message, status_code):
    """This function makes a response for the value error when an inaccurate date format is provided"""
    return make_response(jsonify({
        'status': status,
        'message': message
    })), status_code