# Authentication Token

For authentication we send a token in header. This token is an firebase id token.

Key for the token in header is `AUTHORIZATION`

# API Request Format

1. `get_reply_suggestions`

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
           "other_than": [
               {
                   "message": "String"
               }
           ]
       }
   ```

   1. `word_count` is optional if we skip that, it will generate a short reply
   2. `reply_tone` is optional if we skip that, it will generate a reply in same tone
   3. `other_than` is optional

2. `change_tone`
   ```
   {
       "messages": [
           {
               "message": "String"
           },
           {
               "message": "String"
           },
           {
               "message": "String"
           }
       ],
       "reply_tone": "String",
       "reply_from": "String",
       "word_count": number
   }
   ```
   1. `word_count` is optional if we skip that, it will generate a short reply. We can use this parameter to generate longer replies.
   2. `reply_tone` is optional, we can skip it to generate more replies
