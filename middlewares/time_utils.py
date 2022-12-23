from datetime import datetime


def get_dd_mm_yy():
    date = datetime.now()
    return date.strftime("%d-%m-%y")


def get_mm_yy():
    date = datetime.now()
    return date.strftime("%m-%y")
