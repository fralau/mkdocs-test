# MkDocs-Test

A solid testing framework for [MkDocs](https://www.mkdocs.org/) 
projects and plugins.

- [Github repository](https://github.com/fralau/mkdocs-test).
- MkDocs-Test is open source (MIT License).

### Why MkDocs-Test?

Since the beginning, the quickest way to check whether an MkDocs project
displays correctly, for maintainers of 
an [MkDocs](https://www.mkdocs.org/) website project
(or developers of an [MkDocs plugin](https://www.mkdocs.org/dev-guide/plugins/)),
has been:

1. Initially, to run `mkdocs serve` to start a local web server,
   navigate the pages, modify the Markdown pages and watch "what happens" 
   (interactive editing).
2. Later, to run `mkdocs build` (possibly with the `--strict` option)
   before deploying the new version of your static website.


However, a plain command `mkdocs build` has the following issues:

- It has a binary result: it worked or it didn't.
- It doesn't perform integrity tests on the pages; if something started to
  subtly go wrong, the issue might emerge only later.
- If something went wrong,
  it doesn't necessarily say where, or why.

**How to do non-regression tests, when rebuilding the documentation? 
No one wants to browse the pages of a large website
and manually re-check
the pages one by one, each time a new release is made.**

One solution woud be to write an ad-hoc program to make tests on
the target (HTML) pages; this requires
knowing in advance where those HTML files will be stored and their filenames.
But manually keeping 
track of those pages for large documentation projects,
or for conducting systematic tests, becomes
quickly impractical.

**There has to be a better solution.**



### How MkDocs-Test works

The purpose of Mkdocs-Test is to facilitate the comparison of source pages
(Markdown files) and destination pages (HTML) in an MkDocs project,
to make sure that **what you expect is what you get (WYEIWYG)**.

MkDocs-Test is a test system composed of two parts:

1. An **MkDocs plugin** (`test`): it creates a `__test__` directory, 
  which will contain the data necessary to map the pages of the website.
  The plugin exports MkDocs's `nav` object into that directory.
  

2. A **framework** for conducting the tests. The `DocProject`
  class groups together all the information necessary for the tests on a
  specific MkDocs project.
  It contains a dictionary of Page objects, which are built from the `nav`
  export.

```python
from mkdocs_test import DocProject

# declare the project
# (by default, the directory where the test program resides)
project = DocProject() 
project.build()

assert project.success # the build was successful (returned zero)

# find the page by name, filename or relative pathname:
page = project.get_page('index')

# find the words "hello word", under the header that contains "subtitle"
assert page.find_text_text('hello world', header="subtitle", header_level=2)
```


