"""
Testing the tester

(C) Laurent Franceschetti 2024
"""
import pytest
import os


from mkdocs_test import DocProject, parse_log, list_doc_projects
from mkdocs_test.common import (
        h1, h2, h3, std_print, 
        get_tables, list_markdown_files, find_in_html, find_page)


# ---------------------------
# Initialization
# ---------------------------

"The directory of this file"
REF_DIR = os.path.dirname(os.path.abspath(__file__))

"All subdirectories containing mkdocs.yml"
PROJECTS = list_doc_projects(REF_DIR)


def test_functions():
    "Test the low level fixtures"

    h1("Unit tests")
    # Print the list of directories
    h2("Directories containing mkdocs.yml")
    for directory in PROJECTS:
        print(directory)
    print(PROJECTS)
    print()


    # Example usage
    h2("Parse tables")
    SOURCE_DOCUMENT = """
# Header 1
Some text.

## Table 1
| Column 1 | Column 2 |
|----------|----------|
| Value 1  | Value 2  |
| Value 3  | Value 4  |

## Table 2
| Column A | Column B |
|----------|----------|
| Value A  | Value B  |
| Value C  | Value D  |

## Another Section
Some more text.

| Column X | Column Y |
|----------|----------|
| Value X1 | Value Y1 |
| Value X2 | Value Y2 |
"""

    dfs = get_tables(SOURCE_DOCUMENT)

    # Print the list of directories
    print("Dataframes:")
    for header, df in dfs.items():
        print(f"Table under '{header}':")
        print(df)

    # --------------------
    # Test parsing
    # --------------------
    h2("Parsing logs")
    TEST_CODE = """
DEBUG   -  Running 1 `page_markdown` events
INFO    -  [macros] - Rendering source page: index.md
DEBUG   -  [macros] - Page title: Home
DEBUG   -  No translations found here: '(...)/mkdocs/themes/mkdocs/locales'
WARNING -  [macros] - ERROR # _Macro Rendering Error_

_File_: `second.md`

_UndefinedError_: 'foo' is undefined

```
Traceback (most recent call last):
File "snip/site-packages/mkdocs_macros/plugin.py", line 665, in render
DEBUG   -  Copying static assets.
FOOBAR  -  This is a title with a new severity

Payload here.
DEBUG   -  Copying static assets.
INFO    -  [macros - MAIN] - This means `on_post_build(env)` works
"""
    log = parse_log(TEST_CODE)
    print(log)




    h2("Search in HTML (advanced)")

    # Example usage
    html_doc = """
    <html><head><title>Example</title></head>
    <body>
    <h1>Main Header</h1>
    <p>This is some text under the main header.</p>
    <p>More text under the main header.</p>
    <h2>Sub Header</h2>
    <p>Text under the sub header.</p>
    <h1>Another Main Header</h1>
    <p>Text under another main header.</p>
    </body>
    </html>
    """

    print(html_doc)
    print(find_in_html(html_doc, 'more text'))
    print(find_in_html(html_doc, 'MORE TEXT'))
    print(find_in_html(html_doc, 'under the main', header='Main header'))
    print(find_in_html(html_doc, 'under the main', header='Main header'))
    print(find_in_html(html_doc, 'under the', header='sub header'))
    assert 'More text' in find_in_html(html_doc, 'more text')

def test_find_pages():
    """
    Low level tests for search
    """
    h2("Search pages")

    PAGES = ['foo.md', 'hello/world.md', 'no_foo/bar.md', 'foo/bar.md']
    for name in ('foo', 'world', 'hello/world', 'foo/bar'):
        print(f"{name} -> {find_page(name, PAGES)}")
    assert find_page('foo.md', PAGES)         == 'foo.md'
    assert find_page('world', PAGES)          == 'hello/world.md'
    assert find_page('world.md', PAGES)       == 'hello/world.md'
    assert find_page('hello/world', PAGES)    == 'hello/world.md'
    assert find_page('hello/world.md', PAGES) == 'hello/world.md'
    # doesn't accidentally mismatch directory:
    assert find_page('foo/bar.md', PAGES)     != 'no_foo/bar.md'

    

def test_doc_project():
    """
    Test a project
    """
    PROJECT_NAME = 'simple'
    # MYPROJECT = 'simple'
    h1(f"TESTING MKDOCS PROJECT ({PROJECT_NAME})")

    h2("Config")
    myproject = DocProject(PROJECT_NAME)
    config = myproject.config
    print(config)



    h2("Build")
    result = myproject.build()
    assert result == myproject.build_result
    myproject.self_check() # perform an integrity check
    
    h2("Log")
    assert myproject.trace == result.stderr
    std_print(myproject.trace)




    h2("Filtering the log by severity")
    infos = myproject.find_entries(severity='INFO')
    print(f"There are {len(infos)} info items.")
    print('\n'.join(f"  {i} - {item.title}" for i, item in enumerate(infos)))


    h2("Page objects")                          
    for filename, page in myproject.pages.items():
        h3(f"PAGE: {filename}")
        print("- Title:", page.title)
        print("- Heading 1:", page.h1)
        print("- Markdown(start):", page.markdown[:50])










if __name__ == '__main__':
    pytest.main()