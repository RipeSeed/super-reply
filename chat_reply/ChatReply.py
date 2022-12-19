import openai
import os

OPEN_AI_API_KEY = os.environ.get('OPEN_AI_API_KEY')

# load Open AI API key from environment variable
openai.api_key = OPEN_AI_API_KEY

completion = openai.Completion()


def sanitize_output(output: str):
    # remove extra spaces
    return " ".join(output.split())


def generate_message_for_gpt(messages: list, other_than=None, reply_tone=None, reply_from=None, reply_to=None, word_count=None):
    message = f"Read this email thread\n"

    message += f"{messages[0]['from']} says\n {messages[0]['message']}\n"

    last_from = messages[0]['from']
    second_last_from = ""

    for i in range(1, len(messages)):
        item = messages[i]
        message += f"{item['from']} replies to {last_from}\n{item['message']}\n"

        if last_from != item['from']:
            second_last_from = last_from
            last_from = item['from']

    message += f"and offer {'a short' if word_count==None else ''} " + \
        f"option to reply " +\
        f"from {reply_from if reply_from !=None else second_last_from} to {reply_to if reply_to!=None else last_from} " +\
        f"{f'of about {word_count} words' if word_count!=None else ''} "

    if other_than != None:
        message += "other than "+"and ".join([other_than_message['message']
                                              for other_than_message in other_than])

    if reply_tone != None:
        message += f"in {reply_tone if reply_tone else ''} tone:"

    return message


def get_reply_suggestions(messages: list, suggestion_count=3,
                          other_than=None, reply_tone=None, reply_from=None, reply_to=None, word_count=None):
    message = generate_message_for_gpt(
        messages, other_than, reply_tone, reply_from, reply_to, word_count)

    response = completion.create(
        prompt=message, engine="text-davinci-003", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0.5, presence_penalty=0, best_of=suggestion_count,
        max_tokens=2*word_count if word_count != None else 50, n=suggestion_count)

    suggestions = list()
    for choice in response.choices:
        suggestions.append({"message": sanitize_output(choice.text)})

    return suggestions
