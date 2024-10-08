---
# This frontmatter has a comment
message: "Hello world"
---
# Main Page

{{ message }}!

This is to test a very simple case of an MkDocs project,
with macros: {{ apples }} apples at {{ unit_cost }} each,
cost {{ apples * unit_cost }}
(these variables are contained in the `extra` section of `mkdocs.yml`).


