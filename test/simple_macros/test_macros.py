"""
Testing the project

(C) Laurent Franceschetti 2024
"""


import pytest

from mkdocs_test import DocProject



def test_pages():
    project = DocProject()
    project.build(strict=False)
    # did not fail
    return_code = project.build_result.returncode
    assert not return_code, "Failed when it should not" 



    # ----------------
    # First page
    # ----------------


    page = project.get_page('index')
    print("Plain text:", page.plain_text)
    print("---")
    assert page.html
    print(dir(page))
    print("Page source:", page.source)
    print("---")
    
    assert page.is_markdown_rendered()
    # another way of saying it:
    assert page.markdown.strip() not in page.source.markdown
    


    # ----------------
    # Second page
    # ----------------
    # there is intentionally an error (`foo` does not exist)
    page = project.get_page('second')
    assert page.meta.foo == "Hello world"
    assert "second page" in page.plain_text
    assert page.find('second page',header="subtitle", header_level=2)


    




    