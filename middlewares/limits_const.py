import math
import os

suggestions_limits = {
    "FREE_USER_LIMIT_DAILY": int(os.environ.get('SUGESSION_DAILY_LIMIT', 5)),
    "FREE_USER_LIMIT_MONTHLY": int(os.environ.get('SUGESSION_MONTHLY_LIMIT', 75))
}

change_tone_limits = {
    "FREE_USER_LIMIT_DAILY": math.inf
}
