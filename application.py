from flask import Flask, request
from chat_reply import ChatReply

application = Flask(__name__)


@application.route("/get_reply_suggestions", methods=["GET"])
def get_reply_suggestions():
    messages = request.get_json()
    suggestions = ChatReply.get_reply_suggestions(messages)
    return suggestions


@application.route("/", methods=['GET'])
def index():
    return "Send a get request to the get_reply_suggestions endpoint"


if __name__ == "__main__":
    application.run(debug=True)
