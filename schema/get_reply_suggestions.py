schema = {
    "type": "object",
    "properties": {
        "messages": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                    },
                    "from": {
                        "type": "string",
                    },
                },
                "required": ["message", "from"]
            }
        },
        "reply_tone": {"type": "string"},
        "reply_from": {"type": "string"},
        "reply_to": {"type": "string"},
        "word_count": {"type": "number", "minimum": 1}
    },
    "required": ["messages", "reply_from", "reply_to"]
}
