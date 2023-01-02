import math
import os

suggestions_limits = {
    "FREE_USER_LIMIT_DAILY": int(os.environ.get('SUGESSION_DAILY_LIMIT', 5)),
    "FREE_USER_LIMIT_MONTHLY": int(os.environ.get('SUGESSION_MONTHLY_LIMIT', 75))
}

change_tone_limits = {
    "FREE_USER_LIMIT_DAILY": math.inf
}

word_limits = {
    "FREE_USER_WORD_LIMIT": int(os.environ.get('FREE_USER_WORD_LIMIT', 10000)),
    "PAYED_USER_WORD_LIMIT": int(os.environ.get('PAYED_USER_WORD_LIMIT', -1))
}

if word_limits['PAYED_USER_WORD_LIMIT'] < 0:
    word_limits['PAYED_USER_WORD_LIMIT'] = math.inf
