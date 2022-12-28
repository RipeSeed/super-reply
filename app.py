from firebase_init import *
from schema import change_tone, get_reply_suggestions
import os
from flask_expects_json import expects_json, ValidationError
from flask_cors import CORS

from middlewares.suggestion_request_count import suggestion_request_count_middleware
from middlewares.change_tone_request_count import change_tone_request_count_middleware
from middlewares.input_limit import input_limit_middleware
from middlewares.auth import firebase_auth_middleware
from middlewares.limit_change_tone_requests import limit_change_tone_requests_middleware
from middlewares.limit_suggestion_requests import limit_suggestion_requests_middleware
from middlewares.user_payment import user_payment_middleware

from chat_reply import ChatReply
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

DEFAULT_SUGESSION_COUNT = 3
CORS_WHITE_LIST = os.environ.get('CORS_WHITE_LIST')
CORS(app, origins=CORS_WHITE_LIST, allow_headers=CORS_WHITE_LIST)


@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({'error': original_error.message}), 400)
    # handle other "Bad Request"-errors
    return error


@app.route("/get_reply_suggestions", methods=["POST"])
@expects_json(get_reply_suggestions.schema)
@firebase_auth_middleware
@user_payment_middleware
@input_limit_middleware
@limit_suggestion_requests_middleware
@suggestion_request_count_middleware
def get_reply_suggestions():
    body = request.get_json()
    messages = body['messages']
    user_email = body['user_email']
    suggestion_count = body.get('suggestion_count', DEFAULT_SUGESSION_COUNT)
    word_count = body.get('word_count')
    reply_tone = body.get('reply_tone', 'same')
    other_than = body.get('other_than')
    reply_from = body.get('reply_from')
    reply_to = body.get('reply_to')

    suggestions = ChatReply.get_reply_suggestions(
        user_email, messages, suggestion_count, other_than, reply_tone, reply_from, reply_to, word_count)

    response = make_response(suggestions)

    if request.json.get('remaining_emails_daily') != None:
        response.headers['remaining_emails_daily'] = request.json['remaining_emails_daily']

    if request.json.get('remaining_emails_monthly') != None:
        response.headers['remaining_emails_monthly'] = request.json['remaining_emails_monthly']

    return response


@app.route("/change_tone", methods=["POST"])
@expects_json(change_tone.schema)
@firebase_auth_middleware
@user_payment_middleware
@input_limit_middleware
@limit_change_tone_requests_middleware
@change_tone_request_count_middleware
def change_tone():
    body = request.get_json()
    messages = body['messages']
    user_email = body['user_email']
    suggestion_count = body.get('suggestion_count', DEFAULT_SUGESSION_COUNT)
    word_count = body.get('word_count')
    reply_tone = body.get('reply_tone', 'same')
    other_than = body.get('other_than')
    reply_from = body.get('reply_from')
    reply_to = body.get('reply_to')

    suggestions = ChatReply.change_tone(
        user_email, messages, suggestion_count, other_than, reply_tone, reply_from, reply_to, word_count)

    return suggestions


@app.route("/", methods=['GET'])
def index():
    return "Send a get request to the get_reply_suggestions endpoint"


if __name__ == "__main__":
    app.run()
