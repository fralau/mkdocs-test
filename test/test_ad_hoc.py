"""
Testing a simple project which is built ad hoc
(programmatically)

(C) Laurent Franceschetti 2025 
"""
import time

import pytest

from mkdocs_test import DocProject, lorem_ipsum
from mkdocs_test.common import h1, h2, h3





def test_pages():
    project = DocProject("ad_hoc", new=True)
    project.clear()
    time.sleep(2) # so that we can see the files disappear
    project.add_source_page("index.md","""
            # Main Page

            Hello world!

            This is to test a very simple case of an MkDocs project,
            with two pages.
 
            """)
    project.add_source_page("second.md", f"""
            # Second page

            ## This is a subtitle

            This is a second page.


            ## Second header of level two

            This is more text.
                            
            {lorem_ipsum(3, '            ')}

            Hello.
            """, 
            meta={'foo':'Hello world'})
    

    project.make_config(site_name="Simple ad-hoc test site",
                        theme='mkdocs')


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
    assert page, f"Page '{pagename}' does not exist in {project.pages}"
    print("Plain text\n:", page.plain_text)
    


    # ----------------
    # Second page
    # ----------------
    # there is intentionally an error (`foo` does not exist)
    pagename = 'second'
    h2(f"Testing: {pagename}")
    page = project.get_page(pagename)
    assert page, f"Page '{pagename}' does not exist in {project.pages}"
    assert page.meta.foo == "Hello world"
    assert "second page" in page.plain_text
    assert page.find_text('second page',header="subtitle", header_level=2)
    print("Plain text\n:", page.plain_text)

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

    print("Delete:")
    project.delete()