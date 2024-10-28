"""
Testing the project

(C) Laurent Franceschetti 2024
"""


import pytest

from mkdocs_test import DocProject
from mkdocs_test.common import h1, h2, h3





def test_pages():
    project = DocProject()
    project.build(strict=False)

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
    


    # ----------------
    # Second page
    # ----------------
    # there is intentionally an error (`foo` does not exist)
    pagename = 'second'
    h2(f"Testing: {pagename}")
    page = project.get_page(pagename)
    assert page.meta.foo == "Hello world"
    assert "second page" in page.plain_text
    assert page.find_text('second page',header="subtitle", header_level=2)


    # test find_header() method
    assert page.find_header('subtitle', 2) # by level
    assert not page.find_header('subtitle', 3)
    assert page.find_header('subtitle') # all levels

    # test find_all; all headers of level 2:
    headers = page.find_all('h2')
    assert len(headers) == 2
    print("Headers found:", headers)
    assert "Second header" in headers[1].string
    # check that find also works:
    assert page.find('h2').string == headers[0].string


    
def test_strict():
    "This project must fail"
    project = DocProject()

    # it must not fail with the --strict option,
    project.build(strict=True)
    assert not project.build_result.returncode, "Failed when it should not"



    