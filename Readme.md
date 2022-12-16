# API Request Format

```
    {
        "messages": [
            {
                "message": "String",
                "from": "String",
                "time": "String"
            }
        ],
        "suggestion_count": number,
        "word_count": number,
        "reply_tone": "String"
    }
```

1. `word_count` is optional if we skip that, it will generate a short reply
2. `reply_tone` is optional if we skip that, it will generate a reply in same tone

# OpenAI Models that have Results for this Problem

## Impressive Result

- davinci-instruct-beta
- davinci
- text-babbage-001

## Average Results

- text-similarity-curie-001
- ada-search-query
