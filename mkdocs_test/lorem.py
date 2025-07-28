"""
Lorem ipsum generator
"""


import random
import textwrap

# Constant for identifying source call
CALL_TAG = 'lorem_ipsum('

# Sentence templates and vocabulary pool
SENTENCE_TEMPLATES = [
    "Lorem ipsum dolor sit amet, {tail}.",
    "Sed do eiusmod tempor {action} ut labore et dolore magna aliqua.",
    "Ut enim ad minim veniam, {phrase}, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    "Duis aute irure dolor in reprehenderit in {setting} velit esse cillum dolore eu fugiat nulla pariatur.",
    "Excepteur sint occaecat cupidatat {effect}, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    "{intro} consectetur adipiscing elit.",
    "Aenean euismod bibendum laoreet. {extra}"
]

WORD_CHOICES = {
    "tail": ["consectetur adipiscing elit", "accumsan et malesuada fames", "commodo viverra maecenas accumsan"],
    "action": ["incididunt", "aliquip tempor", "commodo consequat", "reliquaverit noditer"],
    "phrase": ["quis minim veniam", "quis nisi", "velit esse"],
    "setting": ["voluptate", "laboris", "exercitation"],
    "effect": ["non proident", "culpa magna", "tempor incididunt", 'nolenter excpidierunt'],
    "intro": ["Maecenas", "Phasellus", "Integer", "Boticellus"],
    "extra": ["Donec vitae sapien ut libero", "Curabitur blandit tempus porttitor", "Nulla vitae elit libero"]
}

def generate_sentence(template):
    return template.format(**{
        key: random.choice(WORD_CHOICES[key])
        for key in WORD_CHOICES if f'{{{key}}}' in template
    })




import textwrap

def lorem_ipsum(paragraphs: int = 1, indent: str = '', width: int = 60) -> str:
    """
    Generates wrapped Lorem Ipsum pagraphs with:

    - Only the very first line unindented
    - `indent` (string of blank spaces) applied to all other lines
    - One blank line between paragraphs

    Arguments:
        paragraphs: the no of paragraphs required.
        indent: the indentation for the second line and the next ones.
        width: the width of a line

    Returns:
        Paragraphs of Lorem Ipsum text, optionally indented from the second line.
    """
    all_lines = []
    first_line_used = False

    for _ in range(paragraphs):
        # Generate raw paragraph text
        sentences = [generate_sentence(random.choice(SENTENCE_TEMPLATES))
                     for _ in range(random.randint(4, 7))]
        paragraph = ' '.join(sentences)

        # Wrap the paragraph text
        wrapped = textwrap.wrap(paragraph, width=width)

        # Apply indent logic
        for i, line in enumerate(wrapped):
            if not first_line_used:
                all_lines.append(line)
                first_line_used = True
            else:
                all_lines.append(f"{indent}{line}")

        # Add two blank lines *after* the current paragraph
        all_lines.append('')

    return '\n'.join(all_lines).rstrip()





if __name__ == "__main__":
    # Your test or main execution logic here
    print(lorem_ipsum(2, '            '))
