import openai
import os
from .generate_message import for_change_tone, for_reply_suggestions
from .utils import sanitize_output

OPEN_AI_API_KEY = os.environ.get('OPEN_AI_API_KEY')

# load Open AI API key from environment variable
openai.api_key = OPEN_AI_API_KEY

completion = openai.Completion()


def get_reply_suggestions(messages: list, suggestion_count=3,
                          other_than=None, reply_tone=None, reply_from=None, reply_to=None, word_count=None):
    message = for_reply_suggestions(
        messages, other_than, reply_tone, reply_from, reply_to, word_count)

    response = completion.create(
        prompt=message, engine="text-davinci-003", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0.5, presence_penalty=0, best_of=suggestion_count,
        max_tokens=2*word_count if word_count != None else len(message.split(' ')), n=suggestion_count)

    suggestions = list()
    for choice in response.choices:
        suggestions.append({"message": sanitize_output(choice.text)})

    return suggestions


def change_tone(messages: list, suggestion_count=3,
                other_than=None, reply_tone=None, reply_from=None, reply_to=None, word_count=None):
    message = for_change_tone(messages, other_than,
                              reply_tone, reply_from, reply_to, word_count)

    response = completion.create(
        prompt=message, engine="text-davinci-003", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0.5, presence_penalty=0, best_of=len(messages),
        max_tokens=2*word_count if word_count != None else len(message.split(' ')), n=suggestion_count)

    suggestions = list()
    for choice in response.choices:
        suggestions.append({"message": sanitize_output(choice.text)})

    return suggestions
