import openai
import os

OPEN_AI_API_KEY = os.environ.get('OPEN_AI_API_KEY')

# load Open AI API key from environment variable
openai.api_key = OPEN_AI_API_KEY

completion = openai.Completion()


def generate_message_for_gpt(messages: list, suggestion_count: int):
    message = f"Read this email thread"

    message += f"{messages[0]['from']} says\n {messages[0]['message']}\n"

    last_from = messages[0]['from']
    second_last_from = ""

    for i in range(1, len(messages)):
        item = messages[i]
        message += f"{item['from']} replies to {last_from}\n{item['message']}\n"

        if last_from != item['from']:
            second_last_from = last_from
            last_from = item['from']

    message += f"and offer {second_last_from} short option to reply\n"

    return message


def get_reply_suggestions(messages: list, suggestion_count=3):
    message = generate_message_for_gpt(messages, suggestion_count)

    reply = completion.create(
        prompt=message, engine="text-davinci-003", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0.5, presence_penalty=0, best_of=suggestion_count,
        max_tokens=100, n=suggestion_count)

    suggestions = list()
    for choice in reply.choices:
        suggestions.append({"message": choice.text})

    return suggestions