# API Reference for MkDocs Test

## Introduction

This page describes components of the MkDocs-Test API used by testing
components.

A single MkDocs **project** contains a number of **pages**. 
Each page is a composite of the Markdown version, the metadata,
and the fully formed HTML page that will be displayed on a browser.

## Class: DocProject 

### :::mkdocs_test.DocProject
    selection:
        members:
            - __init__
            - project_dir
            - docs_dir
            - test_dir
            - config_file
            - config
            - get_plugin
            - build
            - build_result
            - success
            - pages
            - get_page
            - trace
            - log
            - log_severities
            - find_entries
            - find_entry
            - self_check

## Class: MkDocsPage

### :::mkdocs_test.MkDocsPage

## Class: LogEntry

This Dataclass describes the attributes of a log entry.

### :::mkdocs_test.LogEntry