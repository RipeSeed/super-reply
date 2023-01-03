import math
import os


def __parse_limit(limit):
    try:
        return int(limit)
    except:
        return math.inf


suggestions_limits = {
    "FREE_USER_LIMIT_DAILY": __parse_limit(os.environ.get('SUGESSION_DAILY_LIMIT', 5)),
    "FREE_USER_LIMIT_MONTHLY": __parse_limit(os.environ.get('SUGESSION_MONTHLY_LIMIT', 75))
}

change_tone_limits = {
    "FREE_USER_LIMIT_DAILY": math.inf
}

word_limits = {
    "FREE_USER_WORD_LIMIT": __parse_limit(os.environ.get('FREE_USER_WORD_LIMIT', 10000)),
    "PAYED_USER_WORD_LIMIT": __parse_limit(os.environ.get('PAYED_USER_WORD_LIMIT'))
}
