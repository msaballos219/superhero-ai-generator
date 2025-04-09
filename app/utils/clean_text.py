import re


def clean_generated_text(raw_text):
    # Remove HTML tags with regex
    clean_text = re.sub(r'<.*?>', '', raw_text)

    # Remove Markdown bold markup (**text**)
    clean_text = re.sub(r'\*\*(.*?)\*\*', r'\1', clean_text)

    # Removes '###' and any trailing spaces
    clean_text = re.sub(r'###\s*', '', clean_text)

    # strip excessive whitespace or leading/trailing spaces
    clean_text = clean_text.strip()

    return clean_text