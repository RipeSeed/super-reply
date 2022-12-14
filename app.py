from flask import Flask, request
from chat_reply import ChatReply

app = Flask(__name__)


@app.route("/get_reply_suggestions", methods=["GET"])
def get_reply_suggestions():
    messages = request.get_json()
    suggestions = ChatReply.get_reply_suggestions(messages)
    return suggestions


if __name__ == "__main__":
    app.run(debug=True)
