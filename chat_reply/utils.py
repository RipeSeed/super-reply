import re


def sanitize_email(string: str):
    string = re.sub(r'<img[^>]*>', '', string)
    string = re.sub(r'<video[^>]*>', '', string)
    string = re.sub(r'<svg[^>]*>', '', string)

    # Remove gifs
    string = re.sub(r'\.gif', '', string)

    # Remove signatures
    string = re.sub(r'--\s*\n.*', '', string)

    # Remove links
    string = re.sub(r'https?://[^\s]+', '', string)

    return " ".join(string.split())


def sanitize_output(output: str):
    # remove extra spaces
    return output.strip()
