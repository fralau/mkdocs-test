# --------------------------------------------
# Main part of the plugin
# Defines the MacrosPlugin class
#
# Laurent Franceschetti (c) 2018
# MIT License
# --------------------------------------------

import os
import json
import logging

from bs4 import BeautifulSoup 
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from super_collections import SuperDict

from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page
from mkdocs.structure.nav import Navigation
try:
    from mkdocs.plugins import event_priority
except ImportError:
    event_priority = lambda priority: lambda f: f  # No-op fallback

from .common import TEST_DIRNAME, DOCS_DEFAULT_DIRNAME, PAGE_MAP, get_frontmatter




LOWEST_PRIORITY = -90


# ------------------------------------------
# Utilities
# ------------------------------------------

log = logging.getLogger(f"mkdocs.plugins.test")

def fmt(*args):
    "Format text for the log"
    items = ['[test] - '] + [str(arg) for arg in args]
    return ' '.join(items)


def convert_object(object) -> SuperDict:
    "Convert an object to a dictionary"
    d = {key: value for key, value in object.__dict__.items()
                if not key.startswith('_') and
                isinstance(value, (str, int, float, dict))}
    return SuperDict(d)

def check_dir(dest_file:str):
    "Check that the directories of a destination file exist"
    os.makedirs(os.path.dirname(dest_file), exist_ok=True)

# ------------------------------------------
# Plugin
# ------------------------------------------
class TestPlugin(BasePlugin):
    """
    This plugin generates information necessary
    for testing MkDocs project
    """

    # ----------------------------
    # Directories
    # ----------------------------

    @property
    def docs_dir(self) -> str:
        "The docs directory (relative to project dir)"
        return self.config.get('docs_dir', DOCS_DEFAULT_DIRNAME)

    @property
    def test_dir(self) -> str:
        "Return the test dir"
        return TEST_DIRNAME


    @property
    def nav(self):
        "Get the nav"
        try:
            return self._nav
        except AttributeError:
            raise AttributeError("Trying to access the nav attribute too early")

    @property
    def source_markdown(self) -> SuperDict:
        "The table raw (target) markdown (used to complement the page table)"
        try:
            return self._source_markdown
        except AttributeError:
            self._source_markdown = SuperDict()
            return self._source_markdown      

    # ----------------------------
    # Pages
    # ----------------------------
    def get_page_map(self) -> SuperDict:
        """
        Recursively build the mapping of pages from 
        self.nav: all pages, created by on_nav().
        """
        pages = []
        for page in self.nav.pages:
            d = convert_object(page)
            d.file = convert_object(page.file)
            pages.append(d)
        return SuperDict({page.file.src_uri: page for page in pages})

    # ----------------------------
    # Handling events
    # ----------------------------
    @event_priority(LOWEST_PRIORITY)
    def on_nav(self, nav, config, files):
        "Set the nav"
        self._nav = nav

    @event_priority(LOWEST_PRIORITY)
    def on_post_build(self, config):
        """
        The most important action: export all pages
        This method is called at the end of the build process
        """
        mapping = self.get_page_map()
        out_file = os.path.join(self.test_dir, PAGE_MAP)
        log.info(fmt("Debug file:", out_file))
        check_dir(out_file)
        with open(out_file, 'w') as f:
            json.dump(mapping, f, indent=4)



