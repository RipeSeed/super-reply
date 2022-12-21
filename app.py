from flask import Flask, request
from chat_reply import ChatReply
from middlewares.auth import firebase_auth_middleware
from flask_cors import CORS
import os

app = Flask(__name__)

CORS_WHITE_LIST = os.environ.get('CORS_WHITE_LIST')
CORS(app, origins=CORS_WHITE_LIST)


@app.route("/get_reply_suggestions", methods=["POST"])
@firebase_auth_middleware
def get_reply_suggestions():
    body = request.get_json()
    messages = body['messages']
    suggestion_count = body['suggestion_count']
    word_count = body.get('word_count')
    reply_tone = body.get('reply_tone')
    other_than = body.get('other_than')
    reply_from = body.get('reply_from')
    reply_to = body.get('reply_to')

    suggestions = ChatReply.get_reply_suggestions(
        messages, suggestion_count, other_than, reply_tone, reply_from, reply_to, word_count)
    return suggestions


@app.route("/change_tone", methods=["POST"])
@firebase_auth_middleware
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
