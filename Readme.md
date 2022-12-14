# Authentication Token

For authentication, you can send a token in the header of the API request. The token is a firebase ID token and the key for the token in the header is AUTHORIZATION.

# API Request Format

There are two types of API requests:

`get_reply_suggestions` and `change_tone`.

## `get_reply_suggestions`

This API request generates reply suggestions based on a list of messages (message thread).

The request body should have the following format:

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
        "reply_tone": "String",
        "reply_from": "String",
        "reply_to": "String",
        "other_than": [
            {
                "message": "String"
            }
        ]
    }
```

- `messages`: An array of objects representing the messages in the email thread. Each object has the following fields:

  - `message`: The body of the message (required).
  - `from`: The name of the sender who sent the message in the thread (required).

- `suggestion_count`: (optional) The number of replies that the engine should generate.
- `word_count`: (optional) The desired length of the generated replies. If this field is omitted, the engine will generate short replies. The minimum allowed value is 1.
- `reply_tone`: (optional) The tone of the generated replies. If this field is omitted, the engine will generate replies in the same tone as the input messages.
- `reply_from`: The sender for the messages that the engine is generating as suggestions. This should be the person using the app (required).
- `reply_to`: The recipient of the message, any person from the email thread (required).
- `other_than`: (optional) An array of objects representing messages that should not be included in the generated replies. Each object has a single field, message, representing the body of the message to exclude.

Response Format:

```
{
  "limits": {
        "remaining_suggestions_daily": 4953,
        "remaining_suggestions_monthly": 9878
    },
  "messages": [
    {"message": "String"}
  ]
}
```

## `change_tone`

This API request generates replies with a different tone based on a list of messages.

The request body should have the following format:

```
   {
        "messages": [
            {
                "message": "String",
                "from": "String",
                "time": "String"
            }
        ],
        "reply_tone": "String",
        "reply_from": "String",
        "word_count": number
        "suggestion_count": number,
        "reply_to": "String",
    }

```

- `messages`: An array of objects representing the messages in the email thread. Each object has a single field, `message`, representing the body of the message (required).
- `reply_tone`: (optional) The desired tone of the generated replies. If this field is omitted, the engine will generate replies with the "same" tone.
- `reply_from`: The sender for the messages that the engine is generating as suggestions. This should be the person using the app.
- `word_count`: (optional) The desired length of the generated replies. If this field is omitted, the engine will generate short replies. The minimum allowed value is 1.

Response Format:

```
{
  "limits": {
        "remaining_suggestions_daily": 4953,
        "remaining_suggestions_monthly": 9878
    },
  "messages": [
    {"message": "String"}
  ]
}
```

## Error Code (API Response)

- **FREE_USER_INPUT_LIMIT**

  When a free sends a thread of 1000+ words

- **INPUT_LIMIT**

  When a payed sends a thread of 5000+ words

- **FREE_USER_TONE_LIMIT_DAILY**

  When a free user reaches limit of 1 change tone per day

- **FREE_USER_SUGGESTION_LIMIT_DAILY**

  When a free user reaches limit of 5 get suggestions per day

- **FREE_USER_SUGGESTION_LIMIT_MONTHLY**

  When a free user reaches limit of 75 get suggestions per month

- **KEY_CHANGED_RETRY**
  Resend the request, reason is old openai key has been used up and has been removed
