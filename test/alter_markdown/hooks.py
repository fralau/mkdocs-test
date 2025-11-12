"""
Hook script for altering the code
"""


MY_VARIABLES = {"x": 5, "y": 12, "message": 'hello world'}


def on_page_markdown(markdown:str, *args, **kwargs) -> str:
  """
  Process the markdown template, by interpolating the variables

  e.g. "{x} and {y}" -> "5 and 12"

  Note:
  -----
    .format(), contrary to f-strings, does not allow inline expressions:
    the expression "{x + y}" won't work.
  """
  raw_markdown = markdown.format(**MY_VARIABLES)
  return raw_markdown

