# Testing large or multiple documentation projects

## Introduction

The purpose of this page is to describe how to test large
or multiple documentation projects.

The instructions for [installation](install.md)
and [basic usage](how_to.md) apply. 


## Multiple documentation projects

Multiple documentation projects typically occur during the development
of MkDocs plugins, where different simple MkDocs projects are each
used to set different features.

```
foo-plugin/
│
├── foo-plugin/
│
└── test/
    └── feature1/
    └── feature2/
    └── feature3/
```

The `test` directory contains the different documentation projects. 

Each documentation directory would then be structured as:

```
feature1/
├── __init__.py
├── mkdocs.yaml
├── docs/
│    ├── index.md
│    └── second.md
└── test_site.py
```

Running `pytest` at the level of each MkDocs directory would
run the test for that website.

However, **running `pytest` at the level of the `test` or even at the
level of the plugin's root directory will collect all tests and run them
one by one**.

You can thus, with one `pytest` command, run all tests for your
project as often as you want.

## Using a test fixture

What you may want to do, is to create your own **fixture**, typically to automate
some feature of a plugin or website that reoccurs.

(A **test fixture** is a series of variables, functions, classes, etc.
that are common to the whole test suite, and facilitate it.)

### Location
If you have only one MkDocs project, you might want to implement the fixture
directly in the test script (`test_site.py`), or in an adjacent file.

If you have multiple projects, it is recommended that you implement it in
the test directory (without forgetting the `__init__.py` file).

```
foo-plugin/
│
├── foo-plugin/
│
└── test/
    └── __init__.py
    └── fixture.py
    └── feature1/
    └── feature2/
    └── feature3/
```

In that case you will be able to write import statements as:

```python
from test.fixture import ...
```

### Subclassing the DocProject and MkDocsPage classes

A good way to use a test fixture is to subclass the DocProject and MkDocsPage
classes, to enrich them with methods and properties that might be
specific for your project.

```Python
from mkdocs_test import DocProject, MkDocsPage


class MyProjectPage(MkDocsPage):
    "Specific"

    def is_foo(self):
            """
            Predicate: check whether the page contains 'foo'
                        (this is a naive example)
            """
            return self.find_text('foo')
    
    ...


class MyDocProject(DocProject):
    "Specific"

    @property
    def pages(self) -> dict[MyProjectPage]:
        "List of pages"
        pages = super().pages
        return {key: MyProject(value) for key, value in pages.items()}

    ...
```

!!! Important
    If you subclass `MkDocsPage`, you **must** re-implement the `pages` property,
    so that the `get_page()` method returns a page object of your own class.

If each of your projects, you can then call:

```python
from test.fixture import MyDocProject, MyProjectPage
```