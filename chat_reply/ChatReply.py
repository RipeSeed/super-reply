import openai
import os

OPEN_AI_API_KEY = os.environ.get('OPEN_AI_API_KEY')

# load Open AI API key from environment variable
openai.api_key = OPEN_AI_API_KEY

completion = openai.Completion()


def sanitize_output(output: str):
    # remove extra spaces
    return " ".join(output.split())


def generate_message_for_gpt(messages: list, reply_tone=None, word_count=None):
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

    message += f"and offer {second_last_from} {'a short' if word_count==None else ''} " + \
        f"option to reply {f'of about {word_count} words' if word_count!=None else ''} "

    if reply_tone != None:
        message += f"in {reply_tone if reply_tone else ''} tone"

    return message


def get_reply_suggestions(messages: list, suggestion_count=3, reply_tone=None, word_count=None):
    message = generate_message_for_gpt(messages, reply_tone, word_count)

    response = completion.create(
        prompt=message, engine="text-davinci-003", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0.5, presence_penalty=0, best_of=suggestion_count,
        max_tokens=2*word_count if word_count != None else 50, n=suggestion_count)

    suggestions = list()
    for choice in response.choices:
        suggestions.append({"message": sanitize_output(choice.text)})

    return suggestions
