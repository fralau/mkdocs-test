"""
Various tests

(C) Laurent Franceschetti 2025
"""
from mkdocs_test.common import strip_ansi_colors


def test_strip_colors():
    "Strip colored text instructions"
    FIND = "\x1b[31m"
    colored_text = "\x1b[31mThis is red\x1b[0m and this is normal"
    assert FIND in colored_text
    clean_text = strip_ansi_colors(colored_text)
    assert isinstance(clean_text, str)
    assert FIND not in clean_text
    print(clean_text)  # Output: This is red and this is normal