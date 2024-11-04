# Installation 

## Installing the plugin

MkDocs-Test is an [MkDocs plugin](https://www.mkdocs.org/dev-guide/plugins/).

### From pypi

```sh
pip install mkdocs-test
```

### Locally (Github)

```sh
pip install .
```


### Installing the test framework

Or, to install the test dependencies (for testing _this_ package,
not your MkDocs projects):

```sh
pip install .[test]
```

This will help you run your tests easily, 
using the [`pytest` framework and command](https://docs.pytest.org/en/stable/):

```sh
pip install pytest
```

### Getting started

Now that the tools are installed, you can proceed to [write and run the tests](how_to.md)
for your MkDocs project.


