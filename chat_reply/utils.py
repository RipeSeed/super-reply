import re


def sanitize_output(output: str):
    # remove extra spaces
    return " ".join(output.split())
