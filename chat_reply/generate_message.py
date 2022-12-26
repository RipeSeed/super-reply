from .utils import sanitize_email


def for_reply_suggestions(messages: list, other_than=None, reply_tone=None, reply_from=None, reply_to=None, word_count=None):
    messages = [
        {**message, "message": sanitize_email(message['message'])} for message in messages]
    message = f"Read this email thread\n"

    message += f"{messages[0]['from']} says\n {messages[0]['message']}\n"

    last_from = messages[0]['from']
    second_last_from = ""

    for i in range(1, len(messages)):
        item = messages[i]
        message += f"{item['from']} replies to {last_from}\n{item['message']}\n"

        if last_from != item['from']:
            second_last_from = last_from
            last_from = item['from']

    message += f"and offer {'a short' if word_count==None else ''} " + \
        f"option to reply " +\
        f"from {reply_from if reply_from !=None else second_last_from} to {reply_to if reply_to!=None else last_from} " +\
        f"{f'of about {word_count} words' if word_count!=None else ''} "

    if other_than != None:
        message += "other than "+"and ".join([other_than_message['message']
                                              for other_than_message in other_than])

    if reply_tone != None:
        message += f"in {reply_tone if reply_tone else ''} tone:"

    return message


def for_change_tone(messages: list, other_than=None, reply_tone=None, reply_from=None, reply_to=None, word_count=None):
    messages = [
        {**message, "message": sanitize_email(message['message'])} for message in messages]
    message = f"Read this email thread\n"

    message += f"{messages[0]['from']} says\n {messages[0]['message']}\n"

    last_from = messages[0]['from']
    second_last_from = ""

    for i in range(1, len(messages)):
        item = messages[i]
        message += f"{item['from']} replies to {last_from}\n{item['message']}\n"

        if last_from != item['from']:
            second_last_from = last_from
            last_from = item['from']

    message += f"and offer {'a short' if word_count==None else ''} " + \
        f"option to reply " +\
        f"from {reply_from if reply_from !=None else second_last_from} to {reply_to if reply_to!=None else last_from} " +\
        f"{f'of about {word_count} words' if word_count!=None else ''} "

    if other_than != None:
        message += "other than "+"and ".join([other_than_message['message']
                                              for other_than_message in other_than])

    if reply_tone != None:
        message += f"in {reply_tone if reply_tone else ''} tone:"

    return message
