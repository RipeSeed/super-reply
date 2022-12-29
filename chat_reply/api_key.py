import os

OPEN_AI_API_KEY = [
    {"key": key, "tokens_count": 0} for key in os.environ.get(
        'OPEN_AI_API_KEY').split('::')
]
