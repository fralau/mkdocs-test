# Performing advanced tests

## Introduction
Beyond the [basic functions](how_to.md), the DocProject objects and Page objects
have other tricks up their sleeve.

For more information, see the [documentation of the API](api.md).

## Reading the configuration file

The `config` attribute contains the detail of the config file
(`mkdocs.yml` or `mkdocs.yaml`).


This object is a [SuperDict](https://github.com/fralau/super-collections#superdicts): 
both a dictionary and an object accessible with its attributes.

Here is a simple example:

```yaml
site_name: My MkDocs Site
nav:
    - Home: index.md
    - About: about.md

theme:
    name: material

markdown_extensions:
    - admonition
    - superfences
```


Here are some examples:

```python
site_name = project.config.site_name

assert config.theme.name == "material"

assert "admonition" in [config.markdown_extensions]
```



## Accessing metadata

The metadata of project are located in the
[`extra` part of the config file](https://www.mkdocs.org/user-guide/configuration/#extra):

```python
for key, value in project.config.extra:
    print(key, value)
```

Through the page object, you can access the metadata of a specific page.

```python
page = project.get_page('index')
assert page.meta.foo = 'hello' # key-value pair in the page's frontmatter
```

## Reading log entries

Sometimes (not always) the information you will need is in the
log. 

- `project.trace` contains the log in a string form. 
- `project.log` contains the log in the form of a list of LogEntry objects.

Here are typical examples of a log:

```
DEBUG   -  Running 1 `page_markdown` events
INFO    -  [macros] - Rendering source page: index.md
DEBUG   -  [macros] - Page title: Home
WARNING -  [macros] - ERROR # _Macro Rendering Error_
```

1. Every entry starts with a severity code (Uppercase).
2. The message is then divided into:
    - severity: the level of the log entry.
    - source: the plugin that generated the log entry;
      to be recognized, it must between brackets and followed by a space,
      an hyphen, and another space
      (e.g. `[macros] - `); if no source is recognized, this attribute 
      will have `None` value.
    - title: the remnant of the first line, e.g. "Page title: Home"
    - payload: the rest of the message, until the next severity code at the
      start of a row.

```python
# search in the trace (naïve)
assert "Cleaning site" in project.trace

# get all WARNING log entries
entries = myproject.find_entries(severity='WARNING')

# get the entry from source 'test', containing 'debug file' (case-insensitive)
entry = project.find_entry('debug file', source='test')
assert entry, "Entry not found"
assert entry.severity == 'INFO'
assert 'debug file' in entry.title
```

!!! Note "Notes"
    1. The concept of *payload* is not standard MkDocs and the core application
    will always write its log entries on one line. However,
    if some plugin uses more than one line of text
    (or you want your plugin to do so), 
    you will be able to exploit this feature, typically **to pass information
    to the testing function that would not otherwise be available**.

    2. The same applies for the *source* (it might help narrow down the
    search of log entries).
       