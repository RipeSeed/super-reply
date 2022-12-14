import openai
from .generate_message import for_change_tone, for_reply_suggestions
from .utils import sanitize_output
from .api_key import load_keys, DEFAULT_OPEN_AI_API_KEY
from .count_request_info import update_request_info


KEY_INDEX = 0


def __choose_api_key():
    global completion, KEY_INDEX
    # choose the API key to use
    KEYS = load_keys()
    if len(KEYS) > 0:
        openai.api_key = KEYS[KEY_INDEX]['key']
    else:
        openai.api_key = DEFAULT_OPEN_AI_API_KEY

    completion = openai.Completion()


def __count_words(messages: list):
    return sum([len(message['message'].split(' '))
                for message in messages])


def get_reply_suggestions(email, messages: list, suggestion_count=3,
                          other_than=None, reply_tone=None, reply_from=None, reply_to=None, word_count=None):
    __choose_api_key()

    message = for_reply_suggestions(
        messages, other_than, reply_tone, reply_from, reply_to, word_count)

    response = completion.create(
        prompt=message, engine="text-davinci-003", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0.5, presence_penalty=0, best_of=suggestion_count,
        max_tokens=2*word_count if word_count != None else 2*(int(len(message.split(' '))/len(messages))), n=suggestion_count)

    suggestions = list()
    for choice in response.choices:
        suggestions.append({"message": sanitize_output(choice.text)})

    update_request_info(email, suggestion_count, words_sent=__count_words(
        messages), words_recieved=__count_words(suggestions))

    return suggestions


def change_tone(email, messages: list, suggestion_count=3,
                other_than=None, reply_tone=None, reply_from=None, reply_to=None, word_count=None):
    __choose_api_key()

    message = for_change_tone(messages, other_than,
                              reply_tone, reply_from, reply_to, word_count)

    response = completion.create(
        prompt=message, engine="text-davinci-003", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0.5, presence_penalty=0, best_of=suggestion_count,
        max_tokens=2*word_count if word_count != None else 2*(int(len(message.split(' '))/len(messages))), n=suggestion_count)

    suggestions = list()
    for choice in response.choices:
        suggestions.append({"message": sanitize_output(choice.text)})

    update_request_info(email, suggestion_count, words_sent=__count_words(
        messages), words_recieved=__count_words(suggestions), change_of_tone=1)

    return suggestions
