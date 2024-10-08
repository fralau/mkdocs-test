"""
Testing the project

(C) Laurent Franceschetti 2024
"""


import pytest

from mkdocs_test import DocProject
from mkdocs_test.common import h1, h2, h3





def test_pages():
    PROJECT = DocProject()
    PROJECT.build(strict=False)

    h1(f"Testing project: {PROJECT.config.site_name}")

    # did not fail
    return_code = PROJECT.build_result.returncode
    assert not return_code, "Failed when it should not" 


    # ----------------
    # Test log
    # ----------------
    print(PROJECT.log)
    entry = PROJECT.find_entry(source='test')
    print("---")
    print("Confirming export:", entry.title)

    # ----------------
    # First page
    # ----------------
    pagename = 'index'
    h2(f"Testing: {pagename}")
    page = PROJECT.get_page(pagename)
    print("Plain text:", page.plain_text)
    


    # ----------------
    # Second page
    # ----------------
    # there is intentionally an error (`foo` does not exist)
    pagename = 'second'
    h2(f"Testing: {pagename}")
    page = PROJECT.get_page(pagename)
    assert page.meta.foo == "Hello world"
    assert "second page" in page.plain_text
    assert page.find('second page',header="subtitle", header_level=2)


    
def test_strict():
    "This project must fail"
    PROJECT = DocProject()

    # it must not fail with the --strict option,
    PROJECT.build(strict=True)
    assert not PROJECT.build_result.returncode, "Failed when it should not"



    