from django.utils.html import strip_tags
import re

def count_words_html(html):
    return count_words(strip_tags(html))


def count_words(text):
    return len(re.findall(r'\b\w+\b', text))