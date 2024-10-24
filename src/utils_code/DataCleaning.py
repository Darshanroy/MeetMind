import re

# Cleaning the text using regular expressions
def clean_text(text):
    """Cleans the text by removing unwanted characters and symbols.

    Args:
    text: The input text to be cleaned.

    Returns:
    The cleaned text.
    """

    # Remove punctuation and special characters except for a few symbols
    allowed_symbols = r"[^a-zA-Z0-9\s\.\,\?\!\-\(\)]"
    text = re.sub(allowed_symbols, '', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text