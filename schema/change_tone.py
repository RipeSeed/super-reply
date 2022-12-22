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
                    }
                },
                "required": ["message"]
            }
        },
        "reply_tone": {"type": "string"},
        "reply_from": {"type": "string"},
        "word_count": {"type": "number", "minimum": 1}
    },
    "required": ["messages"]
}
