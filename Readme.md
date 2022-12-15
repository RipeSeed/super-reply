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
        "suggestion_count": number
        "word_count": number
    }
```

`word_count` is optional if you skip that it will generate a short reply

# OpenAI Models that have Results for this Problem

## Impressive Result

- davinci-instruct-beta
- davinci
- text-babbage-001

## Average Results

- text-similarity-curie-001
- ada-search-query
