<div align="center">

![MkDocs-Test](logo.png)

#  A testing framework (plugin + test fixture)<br>for MkDocs projects

</div>

<!-- To update, run the following command:
markdown-toc -i README.md 
-->

<!-- toc -->

- [A testing framework (plugin + test fixture)for MkDocs projects](#a-testing-framework-plugin--test-fixturefor-mkdocs-projects)
  - [Description](#description)
    - [What problem does it solve?](#what-problem-does-it-solve)
    - [MkDocs-Test](#mkdocs-test)
  - [Usage](#usage)
    - [Installation](#installation)
      - [From pypi](#from-pypi)
      - [Locally (Github)](#locally-github)
    - [Installing the plugin](#installing-the-plugin)
    - [Performing basic tests](#performing-basic-tests)
    - [Tests on a page](#tests-on-a-page)
  - [Performing advanced tests](#performing-advanced-tests)
    - [Reading the configuration file](#reading-the-configuration-file)
    - [Accessing page metadata](#accessing-page-metadata)
    - [Reading the log](#reading-the-log)
  - [License](#license)

<!-- tocstop -->

## Description

### What problem does it solve?

Currently the quickest way for maintainers of 
an [MkDocs](https://www.mkdocs.org/) website project
(or developers of an [MkDocs plugin](https://www.mkdocs.org/dev-guide/plugins/)) 
to check whether an MkDocs project builds correctly, 
is to run `mkdocs build` (possibly with the `--strict` option).

It leaves the following issues open:
- This is a binary proposition: it worked or it didn't.
- It doesn't perform integrity tests on the pages; if something started to
  go wrong, the issue might emerge only later.
- If something went already wrong, it doesn't necessarily say where, or why.

One solution is to write an ad-hoc program to make tests on
the target (HTML) pages; this requires
knowing in advance where those files will be stored.

Manually keeping track of those target files is doable
for small documentation projects;
but for larger ones, or for conducting systematic tests, it becomes
quickly impractical.



### MkDocs-Test
The purpose of Mkdocs-Test is to facilitate the comparison of source pages
(Markdown files) and destination pages (HTML) in an MkDocs project.

MkDocs-Test is a framework composed of two parts:

- an MkDocs plugin (`test`): it creates a `__test__` directory, 
  which contains the data necessary to map the pages of the website.

- a framework for conducting the test. The `DocProject`
  class groups together all the information necessary for the tests on a
  specific MkDocs project. 


> 📝 **Technical Note** <br> The plugin exports the `nav` object,
> in the form of a dictionary of Page objects.

## Usage

### Installation 

#### From pypi

```sh
pip install mkdocs-test
```

#### Locally (Github)

```sh
pip install .
```

Or, to install the test dependencies (for testing _this_ package,
not MkDocs projects):

```sh
pip install .[test]
```

### Installing the plugin

> ⚠️ **The plugin is a pre-requisite** <br> The framework will not work
> without the plugin (it exports the pages map into the
> `__test__` directory).

Declare the `test` plugin in your config file (typically `mkdocs.yml`):

```yaml
plugins:
  - search
  - ...
  - test
```

### Performing basic tests

The choice of testing tool is up to you (the examples in this package 
were tested with
[pytest](https://docs.pytest.org/en/stable/)).

```python
from mkdocs_test import DocProject

project = DocProject() # declare the project
                       # (by default, the directory where the program resides)
project.build(strict=False, verbose=False)
              # build the project; these are the default values for arguments

assert project.success # return code of the build is zero (success) ?
print(project.build_result.returncode) # return code from the build

# perform automatic integrity checks (do pages exist?)
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
assert page.find('second page', header="subtitle", header_level=2)
```

> ⚠️ **Two markdown versions** <br>  `page.markdown`
> contains the markdown after possible transformations
> by plugins; whereas `page.source.markdown` contains the exact
> markdown in the file.
>
> If you wish to have the complete source file (including the frontmatter), 
> use `page.source.text`.



## Performing advanced tests

### Reading the configuration file

```python
print(project.config.site_name)


```

### Accessing page metadata

```python
page = project.get_page('index')
assert page.meta.foo = 'hello' # key-value pair in the page's frontmatter
```

### Reading the log

```python
# search in the trace (naïve)
assert "Cleaning site" in project.trace

# get all WARNING log entries
entries = myproject.find_entries(severity='WARNING')

# get the entry from source 'test', containing 'debug file' (case-insensitive)
entry = project.find_entry('debug file', source='test')
assert entry, "Entry not found"
```

## License

MIT License