
# How to get started

While the choice of testing tool is up to you, the examples in this package 
work with [pytest](https://docs.pytest.org/en/stable/).

For detailed information, see the [documentation of the API](api.md).

## Setting up your environment 
1. [Install MkDocs-Test and pytest](install.md).
2. Declare the `test` plugin in your config file (typically `mkdocs.yml`)
    ```yaml
    plugins:
    - search
    - ...
    - test
    ```
3. Create an empty `__init__.py` in the root directory of your project
   (at the same level of your `mkdocs.yaml` program.)
   That will turn your your directory into a Python package
   (this will be convenient for pytest).
4. Create your test program, e.g. `test_site.py`. Any name should
   do, as long as it contains the "test" word.
5. In your `.gitignore` file, make sure that you have a directive
    to exclude the `__test` directory (such as `__*/`), as there
    is likely no point in versioning it.

!!! Important
    **Declaring the plugin is a pre-requisite.** The framework will abort
    if it can't find the plugin (which exports the pages map into the
    `__test__` directory). If that happens, 
    it will helpfully ask you to declare it.
    
    While creating the `__init__.py` is not strictly mandatory, it will
    make your life much easier when using pytest.

## Basic tests

### Building the project

You are now going to programmatically build the MkDocs project
(i.e. the equivalent of `mkdocs build`).

```python
from mkdocs_test import DocProject

project = DocProject() # declare the project
              # (by default, the directory where the program resides)
project.build(strict=False, verbose=False)
              # build the project; 
              # these are the default values for arguments

assert project.success # check that return code is zero (success)

print(project.build_result.returncode) # return code from the build

# Optional: perform automatic integrity checks (do pages exist?)
project.self_check()

```
### Tests on a page

Each page of the MkDocs project can be tested separately

```python
# find the page by relative pathname:
page = project.pages['index.md']

# find the page by name, filename or relative pathname:
page = project.get_page('index')

# easy, and naïve search on the target html page
assert "hello world" in page.html

# find the words "second page", under the header that contains "subtitle"
# at level 2; arguments header and header_level are optional
# the method returns the text so found (if found)
# the search is case insensitive
assert page.find_text_text('second page', header="subtitle", header_level=2)
```

!!! Note "Two markdown versions"
    `page.markdown` contains the markdown after possible transformations
    by plugins; whereas `page.source.markdown` contains the exact
    markdown in the file.

    If you wish to have the complete source file (including the frontmatter), 
    use `page.source.text`.


### Testing the HTML
You can directly access the `.find()` and `.find_all()` methods 
offered by [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all).  

```python
page = project.get_page('foo')
headers = page.find_all('h2') # get all headers of level 2
for header in headers:
  print(header.string)

script = page.find('script', type="module")
assert 'import foo' in script.string
```

## Launching the tests

The recommended way of launching the tests is with the
[pytest framework](https://docs.pytest.org/en/stable/).

If you have set your local directory at the root of the your documentation
project and your test program is properly named (here: `test_site.py`), 
then the pytest command will :

```sh
> pytest
=============================== test session starts ===============================
platform darwin -- Python 3.10.11, pytest-8.3.3, pluggy-1.5.0
rootdir: ~/home/joe/mkdocs-test
...
plugins: anyio-4.3.0
collected 2 items

test_site.py ..                                                             [100%]

================================ 2 passed in 4.48s ================================
```

In the most basic form, no configuration file is needed.

## More advanced tests

For more advanced tests, see the [specific section](advanced.md).