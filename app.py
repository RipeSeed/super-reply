from flask import Flask, request
from chat_reply import ChatReply

app = Flask(__name__)


@app.route("/get_reply_suggestions", methods=["GET"])
def get_reply_suggestions():
    body = request.get_json()
    messages = body['messages']
    suggestion_count = body['suggestion_count']
    word_count = body.get('word_count')
    reply_tone = body.get('reply_tone')
    other_than = body.get('other_than')

    suggestions = ChatReply.get_reply_suggestions(
        messages, suggestion_count, other_than, reply_tone, word_count)
    return suggestions


@app.route("/", methods=['GET'])
def index():
    return "Send a get request to the get_reply_suggestions endpoint"


if __name__ == "__main__":
    app.run()
