# Testing for Developers

_ As of version 0.5.6_

## Introduction

This page is intended especially for **developers** around MkDocs, typically of plugins.

The purpose is to give them indications on how to create a complete
MkDocs project programmatically, then build its (as with a manual `mkdocs build` command)
and then delete it.

In other words, instead of manually writing an MkDocs project a config file and the pages as markdown,
the whole documentation project (config file and pages) is described in the same Python program 
as the code for testing.

The advantage of building an MkDocs project and testing it with with a **self-contained program**
(rather than writing the files one by one, manually), 
is that it becomes possibles to create a larger number of test cases from a limited number
of components, with only a few changes for each.

## Creating a Self-Contained Test Program

Let's say you want to write a test program called `my_test.py`, to be tested with
[pytest](https://docs.pytest.org/en/stable/).

### Initialization

Your test code is contained within a function whose name starts with `test`.

```python
from mkdocs_test import DocProject

def test_pages():
    # create the project folder "my_test" in a subdirectory
    # relative to the the source file:
    project = DocProject("my_test", new=True)
```

!!! Note "`docs` directory"
    Note that, for simplicity, `docs_dir` (the docs directory) is assumed to be `docs`.
    Do not define it otherwise.

If you want to make sure that all pre-existing pages are deleted:
```python
   project.clear() # delete all pages in the `docs` folder, if they exist
```

### Specifying the config

Creating a config file is straightforward:

```python
    project.make_config(site_name="Simple ad-hoc test site",
                        theme='mkdocs',
                        nav = [
                                {"Home": "index.md"},
                                {"Next page": "second.md"}
                              ]
                        )
```

This will create or overwrite the YAML config file (`mkdocs.yml`).

You can specify each main entry of the config file in this way.

If you wish you can insert some code directly as YAML,
which makes it cleaner for more complex entries, such as `nav`:

```python
    project.make_config(site_name="Simple ad-hoc test site",
                        theme='mkdocs',
                        content="""
                            nav:
                                - Home: index.md
                                - Next page: second.md
                            """)
```

The function will dedent the YAML code automatically,
so that it is aligned to the left.

!!! Note
    **The plugin `test` is necessary to make the framework
    work.**

    To make your life easier:
    
    - If you don't specify any `plugin` entry in the config file, that entry will be created
      with the the `search` and `test` plugins.
    - If you specified a `plugin` entry then a line 
      `test will be
      added automatically, if missing.
    

## Adding Pages

### Simple Case
To add a source page:

```python
    project.add_source_page("index.md","""
            # Main Page

            Hello world!

            This is to test a very simple case of an MkDocs project,
            with two pages.
 
            """,
            meta={'foo':'Hello world'})
```

The function will appropriately dedent the content.

The optional `meta` argument adds a YAML header to the page.

This is the resulting YAML:

```yaml
---
foo: Hello world
---

# Main Page

Hello world!

This is to test a very simple case of an MkDocs project,
with two pages.
```

## Performing tests
You can then build the target and test the pages as [in the basic how-to](how_to.md/#basic-tests).

```python
project.build()

page = project.get_page('index')
assert page.find_header('Main Page', 1)
```

## Deleting a project

You can delete the **directory** with all the
**files** (markdown, etc.)
of the documentation project that you just created.

```python
project.delete()
```

The DocProject object will become inoperable.

!!! Warning
    Use with caution. This deletes the project directory
    with **all the files** contained in it.

    In principle you should do this only with an MkDocs
    project that you created programmatically.

    If you wish to delete only the files in the `docs` directory
    (with the markdown pages, etc),
    use `project.clear()`.

## Lorem Ipsum Generator
The package exports a random Lorem Ipsum generator created especially for this purpose.

In its simplest form, a call to `lorem_ipsum()` generates one paragraph,
and `lorem_ipsum(3)` will generate 3 ones.

### Use within an f-string
A typical use is within an f-string, for generating a page.

!!! Warning
    However, in the case this function is used within an indented string,
    the second line and the following one would be aligned to the left margin
    this would prevent the deindentation from working,
    and MkDocs would not render the Markdown properly into
    HTML.

To correct that issue, it is necessary to fill
the second and next lines of the text generated with
blanks at the beginning;

Just add a string of blanks as a second argument:
`lorem_ipsum(2, '            ')`.

For example:

```python
    from mkdocs_test import lorem_ipsum

    project.add_source_page("second.md", f"""
            # Second page
                            
            {lorem_ipsum(2, '            ')}
            """)
```

(To get it right, simply make a copy-paste of the leading blanks in your editor.)

After processing by `.add_source_page()`, this results in:

```markdown
# Second page
Aenean euismod bibendum laoreet. Nulla vitae elit libero
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Aenean euismod bibendum laoreet. Nulla vitae elit libero
Lorem ipsum dolor sit amet, commodo viverra maecenas
accumsan. Sed do eiusmod tempor aliquip tempor ut labore et
dolore magna aliqua. Phasellus consectetur adipiscing elit.

Excepteur sint occaecat cupidatat tempor incididunt, sunt in
culpa qui officia deserunt mollit anim id est laborum.
Integer consectetur adipiscing elit. Sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad
minim veniam, velit esse, quis nostrud exercitation ullamco
laboris nisi ut aliquip ex ea commodo consequat. Phasellus
consectetur adipiscing elit. Ut enim ad minim veniam, quis
nisi, quis nostrud exercitation ullamco laboris nisi ut
aliquip ex ea commodo consequat. Duis aute irure dolor in
reprehenderit in exercitation velit esse cillum dolore eu
fugiat nulla pariatur.
```







