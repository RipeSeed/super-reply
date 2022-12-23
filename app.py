from firebase_init import *
from schema import change_tone, get_reply_suggestions
import os
from flask_expects_json import expects_json, ValidationError
from flask_cors import CORS

from middlewares.suggestion_request_count import suggestion_request_count_middleware
from middlewares.change_tone_request_count import change_tone_request_count_middleware
from middlewares.input_limit import input_limit_middleware
from middlewares.auth import firebase_auth_middleware

from chat_reply import ChatReply
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

CORS_WHITE_LIST = os.environ.get('CORS_WHITE_LIST')
CORS(app, origins=CORS_WHITE_LIST)


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
@input_limit_middleware
@suggestion_request_count_middleware
def get_reply_suggestions():
    body = request.get_json()
    messages = body['messages']
    suggestion_count = body['suggestion_count']
    word_count = body.get('word_count')
    reply_tone = body.get('reply_tone', 'same')
    other_than = body.get('other_than')
    reply_from = body.get('reply_from')
    reply_to = body.get('reply_to')

    suggestions = ChatReply.get_reply_suggestions(
        messages, suggestion_count, other_than, reply_tone, reply_from, reply_to, word_count)
    return suggestions


@app.route("/change_tone", methods=["POST"])
@expects_json(change_tone.schema)
@firebase_auth_middleware
@change_tone_request_count_middleware
def change_tone():
    body = request.get_json()
    messages = body['messages']
    reply_tone = body.get('reply_tone', 'same')
    reply_from = body.get('reply_from')
    word_count = body.get('word_count')

    suggestions = ChatReply.change_tone(
        messages, reply_tone, reply_from, word_count)

    return suggestions


@app.route("/", methods=['GET'])
def index():
    return "Send a get request to the get_reply_suggestions endpoint"


if __name__ == "__main__":
    app.run()
