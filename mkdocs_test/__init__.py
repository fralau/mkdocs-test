# from rich import print
import os
import yaml
import inspect
import subprocess
import re
from dataclasses import dataclass, field
from typing import List
import json
from typing import Any, List

from bs4 import BeautifulSoup


"A dictionary where the keys are also accessible with the dot notation"
from super_collections import SuperDict
from .common import (get_frontmatter, markdown_to_html, get_first_h1,
                find_in_html, find_after, list_markdown_files, find_page,
                run_command, TEST_DIRNAME, DOCS_DEFAULT_DIRNAME, PAGE_MAP) 

# ---------------------------
# Initialization
# ---------------------------

"Command for build"
MKDOCS_BUILD = ['mkdocs', 'build']



def list_doc_projects(directory:str):
    "Make a list of Mkdocs projects"
    # Specify the directory to start the search
    start_dir = directory
    mkdocs_dirs = []
    for entry in os.scandir(start_dir):
        if entry.is_dir():
            files_in_dir = os.listdir(entry.path)
            if 'mkdocs.yml' in files_in_dir or 'mkdocs.yaml' in files_in_dir:
                mkdocs_dirs.append(entry.name)
    return mkdocs_dirs







# ---------------------------
# Log parsing
# ---------------------------

@dataclass
class LogEntry(object):
    """
    Represents a log entry
    """
    
    "Severity (DEBUG, INFO, WARNING)"
    severity: str

    "Source, if available (e.g. [macros])"
    source: str = None

    "Title, first line"
    title: str = None

    "Payload, following lines"
    payload: str = None



def parse_log(mkdocs_log: str) -> list[LogEntry]:
    """
    Parse the log entries, e.g.:

        DEBUG   -  Running 1 `page_markdown` events
        INFO    -  [macros] - Rendering source page: index.md
        DEBUG   -  [macros] - Page title: Home
        WARNING -  [macros] - ERROR # _Macro Rendering Error_

        _File_: `second.md`

        _UndefinedError_: 'foo' is undefined

        ```
        Traceback (most recent call last):
        File "snip/site-packages/mkdocs_macros/plugin.py", line 665, in render
        DEBUG   -  Copying static assets.

    RULES:
    1. Every entry starts with a severity code (Uppercase).
    2. The message is then divided into:
        - source: between brackets, e.g. [macros]
        - title: the remnant of the first line, e.g. "Page title: Home"
        - payload: the rest of the message
    """
    log_entries = []
    current_entry = None
    mkdocs_log = mkdocs_log.strip()

    for line in mkdocs_log.split('\n'):
        match = re.match(r'^([A-Z]+)\s+-\s+(.*)', line)
        if match:
            if current_entry:
                log_entries.append(current_entry)
            severity = match.group(1)
            message = match.group(2)
            source_match = re.match(r'^\[(.*?)\]\s+-\s+(.*)', message)
            if source_match:
                source = source_match.group(1)
                title = source_match.group(2)
            else:
                source = ''
                title = message
            current_entry = {'severity': severity, 
                             'source': source, 
                             'title': title,
                             'payload': []}
        elif current_entry:
            # current_entry['payload'] += '\n' + line
            current_entry['payload'].append(line)
    if current_entry:
        log_entries.append(current_entry)

    # Transform the payloads into str:
    for entry in log_entries:
        entry['payload'] = '\n'.join(entry['payload']).strip()
    return [SuperDict(item) for item in log_entries]

# ---------------------------
# An Mkdocs Documentation project
# ---------------------------
class MkDocsPage(SuperDict):
    "A markdown page from MkDocs, with all its information (source, target)"

    MANDATORY_ATTRS = ['title', 'markdown', 'content', 'meta', 'file']

    def __init__(self, page:dict):
        # Call the superclass's __init__ method
        super().__init__(page)
        for field in self.MANDATORY_ATTRS:
            if field not in self:
                raise AttributeError(f"Missing attribute '{field}'")



    


    @property
    def h1(self):
        "First h1 in the markdown"
        return get_first_h1(self.markdown)


    @property
    def plain_text(self):
        """
        The content, as plain text
        """
        try:
            return self._plain_text
        except AttributeError:
            soup = BeautifulSoup(self.content, "html.parser")
            self._plain_text = soup.get_text()
            return self._plain_text

    
    @property
    def html(self):
        """
        The final HTML code that will be displayed,
        complete with json, etc. (the end product).
        """
        try:
            return self._html
        except AttributeError:
            try:
                with open(self.file.abs_dest_path, 'r') as f:
                    s = f.read()
                self._html = s
                return self._html
            except AttributeError as e:
                # to make sure we don't go into a weird recovery
                # with SuperDict, in case of AttributeError (get_attr)
                raise Exception(e)


    @property
    def source(self) -> SuperDict:
        """
        The source information, drawn from the source file
        (it contains the markdown)
        """
        try:
            return self._source
        except AttributeError:
            try:
                # get the source file and decompose it
                src_filename = self.file.abs_src_path
                assert os.path.isfile(src_filename), f"'{src_filename}' does not exist"
                with open(src_filename, 'r') as f:
                    source_text = f.read()
                markdown, frontmatter, meta = get_frontmatter(source_text) 
                source = {
                    'text': source_text,
                    'markdown': markdown,
                    'frontmatter': frontmatter,
                    'meta': meta
                }
                self._source = SuperDict(source)
                return self._source
            except AttributeError as e:
                # to make sure we don't go into a weird recovery
                # with SuperDict, in case of AttributeError (get_attr)
                raise Exception(e)



    def find(self, pattern: str, 
             header: str = None, header_level: int = None) -> str | None:
        """
        Find a text or regex pattern in the markdown page (case-insensitive).
        
        Arguments
        ---------
        - html: the html string
        - pattern: the text or regex
        - header (text or regex): if specified, it finds it first,
        and then looks for the text between that header and the next one
        (any level).
        - header_level: you can speciy it, if there is a risk of ambiguity.

        Returns
        -------
        The line where the pattern was found, or None
        """
        # it operates on the html
        return find_in_html(self.html,
                            pattern=pattern, 
                            header=header, header_level=header_level)




    # ----------------------------------
    # Predicate functions
    # ----------------------------------

    def is_src_file(self) -> bool:
        """
        Predicate: does the source (Markdown) file exist?
        """
        return os.path.isfile(self.file.abs_src_path)
    

    def is_dest_file(self) -> bool:
        """
        Predicate: does the destination file (HTML) exist?
        """
        return os.path.isfile(self.file.abs_dest_path)


    def is_markdown_rendered(self) -> bool:
        """
        Predicate: "Rendered" means that the raw Markdown 
        is different from the source markdown;
        more accurately, that the source markdown is not 
        contained in the target markdown.

        Please do NOT confuse this with the rendering of Markdown into HTML
        (with templates containing navigation,
        header and footer, etc.).

        Hence "not rendered" is a "nothing happened". 
        It covers these cases: 
        1. No rendering of the markdown has taken place at all
            (no plugin, or plugin inactive, or not instructions within the page). 
        2. A header and/or footer were added to the Markdown code 
            (in `on_pre_page_macros()
            or in `on_post_page_macro()` in Mkdocs-Macros) but the Markdown 
            itself was not modified.
        3. An order to render was given, but there was actually 
           NO rendering of the markdown, for some reason (error case).
        """
        # make sure that the source is stripped, to be sure.
        return self.source.markdown.strip() not in self.markdown
    





class DocProject(object):
    """
    An object that describes the current MkDocs project being tested
    (any plugin).
    """

    def __init__(self, project_dir:str='', path:str=''):
        """
        Initialize the documentation project.

        Designed for pytest: if the path is not defined, 
        it will take the path of the calling program.
        """
        if not path:
            # get the caller's directory
            caller_frame = inspect.stack()[1]
            path = os.path.dirname(caller_frame.filename)
            path = os.path.abspath(path)
        project_dir = os.path.join(path, project_dir)
        self._project_dir = project_dir
        # test existence of YAML file or fail
        self.config_file



        

    @property
    def project_dir(self) -> str:
        "The source directory of the MkDocs project (abs or relative path)"
        return self._project_dir
    
    @property
    def docs_dir(self):
        "The target directory of markdown files (full path)"
        return os.path.join(self.project_dir, 
                            self.config.get('docs_dir', DOCS_DEFAULT_DIRNAME))

    @property
    def test_dir(self):
        "The test directory (full path)"
        return os.path.join(self.project_dir, TEST_DIRNAME) 
    

    
    # ----------------------------------
    # Config file
    # ----------------------------------
 
    @property
    def config_file(self) -> str:
        "The config file"
        try:
            return self._config_file
        except AttributeError:
            # List of possible mkdocs configuration filenames
            CANDIDATES = ['mkdocs.yaml', 'mkdocs.yml']
            for filename in os.listdir(self.project_dir):
                if filename in CANDIDATES:
                    self._config_file = os.path.join(self.project_dir, filename)
                    return self._config_file
            raise FileNotFoundError("This is not an MkDocs directory")
        
    @property
    def config(self) -> SuperDict:
        """
        Get the configuration from the config file.
        All main items of the config are accessible with the dot notation.
        (config.site_name, config.theme, etc.)
        """
        try:
            return self._config
        except AttributeError:
            with open(self.config_file, 'r', encoding='utf-8') as file:
                self._config = SuperDict(yaml.safe_load(file))
            return self._config
        
    def get_plugin(self, name:str) -> SuperDict:
        "Get a plugin config (from the Config file) by its plugin name"
        for el in self.config.plugins:
            if name in el:
                if isinstance(el, str):
                    return SuperDict()
                elif isinstance(el, dict):
                    plugin = el[name]
                    return SuperDict(plugin)
                else:
                    raise ValueError(f"Unexpected content of plugin {name}!")
        return SuperDict(self.config.plugins.get(name))




    

    # ----------------------------------
    # Build
    # ----------------------------------


    def build(self, strict:bool=False,
              verbose:bool=False) -> subprocess.CompletedProcess:
        """
        Build the documentation, to perform the tests

        Arguments:
            - strict (default: False) to make the build fail in case of warnings
            - verbose (default: True), to generate the target_files directory

        Returns:
        (if desired) the low level result of the process 
        (return code and stderr).

        This is not needed, since, those values are stored, and parsed.
        """
        os.chdir(self.project_dir)
        command = MKDOCS_BUILD.copy()
        assert '--strict' not in command
        if strict:
            command.append('--strict')
        if verbose:
            command.append('--verbose')
        print("BUILD COMMAND:", command)
        self._build_result = run_command(*command)
        return self.build_result


    # ----------------------------------
    # Post-build properties
    # Will fail if called before build
    # ----------------------------------
    @property
    def build_result(self) -> subprocess.CompletedProcess:
        """
        Result of the build (low level)
        """
        try:
            return self._build_result
        except AttributeError:
            raise AttributeError("No build result yet (not run)")

    @property
    def success(self) -> bool:
        "Was the execution of the build a success?"
        return self.build_result.returncode == 0




    # ----------------------------------
    # Get the Markdown pages
    # ----------------------------------

    @property
    def page_map_file(self):
        "The page map file exported by the Test plugin"
        filename = os.path.join(self.test_dir, PAGE_MAP)
        if not os.path.isfile(filename):
            raise FileNotFoundError("The pagemap file was not found. " 
                        "Did you forget to declare the `test` plugin "
                        "in the MkDocs config file?")
        return filename

    @property
    def pages(self) -> dict[MkDocsPage]:
        "The dictionary of Markdown pages + the HTML produced by the build"
        try:
            return self._pages
        except AttributeError:
            # build the pages
            with open(self.page_map_file, 'r') as file:
                pages = json.load(file)
            self._pages = {key: MkDocsPage(value) for key, value in pages.items()}
            return self._pages
        
    def get_page(self, name:str) -> MkDocsPage | None:
        """
        Find a name in the list of Markdown pages (filenames)
        using a name (full or partial, with or without extension).
        """
        # get all the filenames of pages:
        filenames = [filename for filename in self.pages.keys()]
        # get the filename we want, from that list:
        filename = find_page(name, filenames)
        # return the corresponding page:
        return self.pages.get(filename)
        
    # ----------------------------------
    # Log
    # ----------------------------------
    @property
    def trace(self) -> str:
        "Return the trace of the execution (log as text)"
        return self.build_result.stderr
    
   

    
    @property
    def log(self) -> List[SuperDict]:
        """
        The parsed trace
        """
        try:
            return self._log
        except AttributeError:
            self._log = parse_log(self.trace)
            # print("BUILT:", self.log)
            return self._log

    @property
    def log_severities(self) -> List[str]:
        """
        List of severities (DEBUG, INFO, WARNING) found
        """
        try:
            return self._log_severities
        except AttributeError:
            self._log_severities = list({entry.get('severity', '#None') 
                                     for entry in self.log})
            return self._log_severities


    def find_entries(self, title:str='', source:str='',
                     severity:str='') -> List[SuperDict]:
        """
        Filter entries according to criteria of title and severity;
        all criteria are case-insensitive.

        Arguments:
            - title: regex
            - source: regex, for which entity issued it (macros, etc.)
            - severity: one of the existing sevirities
        """
        if not title and not severity and not source:
            return self.log
        
        severity = severity.upper()
        # if severity and severity not in self.log_severities:
        #     raise ValueError(f"{severity} not in the list")
        
        filtered_entries = []
        # Compile the title regex pattern once (if provided)
        title_pattern = re.compile(title, re.IGNORECASE) if title else None
        source_pattern = re.compile(source, re.IGNORECASE) if source else None
        
        for entry in self.log:
            # Check if the entry matches the title regex (if provided)
            if title_pattern:
                title_match = re.search(title_pattern, entry.get('title', ''))
            else:
                title_match = True
            # Check if the entry matches the source regex (if provided)
            if source_pattern:
                source_match = re.search(source_pattern, entry.get('source', ''))
            else:
                source_match = True

            # Check if the entry matches the severity (if provided)
            if severity:
                severity_match = (entry['severity'] == severity)
                # print("Decision:", severity_match)
            else:
                severity_match = True
            # If both conditions are met, add the entry to the filtered list
            if title_match and severity_match and source_match:
                filtered_entries.append(entry)
        assert isinstance(filtered_entries, list)
        return filtered_entries


    def find_entry(self, title:str='', 
                   source:str = '',
                   severity:str='') -> SuperDict | None:
        """
        Find the first entry according to criteria of title and severity

        Arguments:
            - title: regex
            - source: regex
            - severity
        """
        found = self.find_entries(title, 
                                  source=source,
                                  severity=severity)
        if len(found):
            return found[0]
        else:
            return None          

    # ----------------------------------
    # Self-check
    # ----------------------------------
    def self_check(self):
        "Performs a number of post-build self-checks (integrity)"
        for page in self.pages.values():
            name = page.file.name
            assert page.markdown, f"'{name}' is empty"
            assert page.is_src_file(), f"source (Markdown) of '{name}' is missing"
            assert page.is_dest_file(), f"destination (HTML) of '{name}' is missing"