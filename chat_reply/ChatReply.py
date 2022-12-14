from dotenv import load_dotenv, dotenv_values
import openai

load_dotenv()

env_values = dotenv_values()
OPEN_AI_API_KEY = env_values['OPEN_AI_API_KEY']

openai.api_key = OPEN_AI_API_KEY

completion = openai.Completion()


def generate_message_for_gpt(messages: list, suggestion_count: int):
    message = f"Please Suggest {suggestion_count} replies for message\n"
    for item in messages:
        message += f"{item['message']}\n"

    message += f"What will should I reply?\n"
    return message


def get_reply_suggestions(messages: list, suggestion_count=3):
    message = generate_message_for_gpt(messages, suggestion_count)
    reply = completion.create(
        prompt=message, engine="davinci", stop=['\n'], temperature=0.9,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=suggestion_count,
        max_tokens=150, n=suggestion_count)
    suggestions = list()
    for choice in reply.choices:
        suggestions.append(choice.text)
    return suggestions
