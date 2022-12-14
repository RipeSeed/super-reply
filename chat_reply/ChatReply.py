import openai
import os

OPEN_AI_API_KEY = os.environ.get('OPEN_AI_API_KEY')

# load Open AI API key from environment variable
openai.api_key = OPEN_AI_API_KEY

completion = openai.Completion()


def generate_message_for_gpt(messages: list, suggestion_count: int):
    message = ""
    for item in messages:
        message += f"{item['from']}: {item['message']}\n"
    return message


def get_reply_suggestions(messages: list, suggestion_count=3):
    message = generate_message_for_gpt(messages, suggestion_count)

    reply = completion.create(
        prompt=message, engine="davinci", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=suggestion_count,
        max_tokens=150, n=suggestion_count)

    suggestions = list()
    for choice in reply.choices:
        suggestions.append({"message": choice.text})

    return suggestions
