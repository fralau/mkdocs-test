# Performing advanced tests

## Introduction
The DocProject objects and Page objects have other tricks up their sleeve.

## Reading the configuration file

The `config` attribute contains the detail of the config file
(`mkdocs.yml` or `mkdocs.yaml`).

```python
print(project.config.site_name)
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

## Reading the log

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
    - source: between brackets, e.g. [macros]
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