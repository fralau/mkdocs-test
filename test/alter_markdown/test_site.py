"""
Testing the project

(C) Laurent Franceschetti 2024
"""


import pytest

from mkdocs_test import DocProject
from mkdocs_test.common import h1, h2, h3

from .hooks import MY_VARIABLES




def test_pages():
    project = DocProject()
    project.build(strict=True)

    h1(f"Testing project: {project.config.site_name}")

    # did not fail
    return_code = project.build_result.returncode
    assert not return_code, "Failed when it should not" 


    # ----------------
    # Test log
    # ----------------
    print(project.log)
    entry = project.find_entry(source='test')
    print("---")
    print("Confirming export:", entry.title)

    # ----------------
    # First page
    # ----------------
    pagename = 'index'
    h2(f"Testing: {pagename}")
    page = project.get_page(pagename)
    print("Plain text:", page.plain_text)

    # it has been altered
    assert page.markdown.strip() != page.source.markdown.strip()
    assert page.is_markdown_rendered() # check that markdown is rendered

    # null test
    assert "foobar" not in page.markdown

    # brute-force testing
    assert "hello world" in page.markdown.lower()

    # check that the values of the variables have been properly rendered:
    assert page.find(MY_VARIABLES['x'], header="Values")
    assert page.find(MY_VARIABLES['y'], header="Values")
    assert page.find(MY_VARIABLES['message'], header="Message")
    


    # ----------------
    # Second page
    # ----------------
    pagename = 'second'
    h2(f"Testing: {pagename}")
    page = project.get_page(pagename)
    assert page
    # not altered
    assert page.markdown.strip() == page.source.markdown.strip() 
    assert not page.is_markdown_rendered()

    




    