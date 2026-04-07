import re

def clean_text(text):
    # Remove patterns like (cid:127)
    text = re.sub(r'\(cid:\d+\)', '', text)

    # Also remove plain cid:127 if any
    text = re.sub(r'cid:\d+', '', text)

    # Remove unwanted special characters
    text = re.sub(r'[^\w\s@.,:]', '', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()