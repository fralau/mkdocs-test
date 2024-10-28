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


    # ----------------
    # Third page
    # check that it handles subdirs correctly
    # ----------------
    page_path = 'other/third.md'
    page = project.pages[page_path] # it is found by its pathname
    assert "# This is a third file" in page.markdown
    
def test_strict():
    "This project must fail"
    project = DocProject()

    # it must not fail with the --strict option,
    project.build(strict=True)
    assert not project.build_result.returncode, "Failed when it should not"



    