"""This module defines the help command of the application."""

from click import echo_via_pager

from ..repl import Command
from .bib import bib


@bib.add("help", "closed-closed")
class Help(Command):
    def execute(self, arguments, session, config, result=None):
        echo_via_pager(HELP)


HELP = """Bibliophant manual
------------------


# Queries

Bibliophant allows to build larger queries out of smaller pieces.
This is similar to the use of the pipe character "|" in Unix shells.
Since bibliophant queries can be invoked directly from such shells,
it was necessary to chose a different symbol for separating the parts
of a pipeline. The sequence " : " was chosen. Note that the spaces
to either side of the colon are necessary.


## Solo queries (closed-closed)

This section presents the commands which cannot be chained together.


`exit`
    Quits the application.

`help`
    Shows this document.
    
`ipython`
    Opens an interactive Python shell.
    Imports various bibliophant modules.
    Established a connection to the database.


All 'edit' commands save changes to the database and to all
the affected JSON files in the collection's record folders.

`edit record <record key>`
    Given the key of a record (article or book),
    opens the record editor.

`edit tag <tag name>`
    Given the name of a tag,
    opens the tag editor.
 
`edit author <author name>`
    Given the name of an author,
    opens the author editor.

`edit publisher <publisher name>`
    Given the name of a (book) publisher,
    opens the publisher editor.

`edit journal <journal name>`
    Given the name of a journal,
    opens the journal editor.


## At-the-beginning (sub-)queries (the closed-producing kind)

This section presents the commands which must appear at the beginning
of a pipeline. They all "produce" one record, which
can be picked up by a following command.

All 'add' and 'import' commands store the supplied data in the database,
and in a JSON file within the created record folder.

`add (article | book) [<path to pdf>]` --> {record}
    Either opens the article or book editor.
    If a path to a PDF file is provided,
    this file is moved into the created record folder.

`import doi <DOI> [<path to pdf>]` --> {record}
    Given a DOI, tries to fetch bibliographic data from the web.
    Opens the article editor (with certain fields already filled in).
    If a path to a PDF file is provided,
    this file is moved into the created record folder.

`import arxiv <arXiv id>` --> {record}
    Given an arXiv id, tries to fetch bibliographic data from the arXiv.
    Opens the article editor (with certain fields already filled in).
    Downloads the eprint and stores it in the created record folder.

`import bib <path to external record folder>` --> {record}
    Given a path to a record folder from another bibliophant collection,
    opens either the article or book editor (with certain fields already filled in).
    If the record folder contains other (usually PDF) files,
    they are copied to the created record folder.


## At-the-beginning sub-queries (more of the closed-producing kind)

This section presents further commands which must appear at the beginning
of a pipeline. They all "produce" at least one record, which
should be picked up by a following command.
It does not make sense to run these commands solo.

`get key <record key>` --> {record}
    Given the key of a record (article or book),
    gets the record from the database,
    and passes it on to the follow-up command.

`get title <record title>` --> {record}
    Given (parts of) the title of a record (article or book),
    gets the record from the database,
    and passes it on to the follow-up command.

`get doi <doi> -->` {record}
    Given the DOI of a record (article or book),
    gets the record from the database,
    and passes it on to the follow-up command.

`get arxiv <arxiv id>` --> {record}
    Given the arXiv id of an article,
    gets the article from the database,
    and passes it on to the follow-up command.


The following command usually "produce" multiple records.
If a positive integer (limit) is supplied as an option,
only the first <limit> most recent results will be passed on.

`get all [<limit>]` --> {records}
    Passes on all or the <limit> most-recently added records.

`get tag <tag name> [<limit>]` --> {records}
    Given the name of a tag,
    gets all records which carry this tag from the database,
    and passes them on to the follow-up command.

`get author <author name> [<limit>]` --> {records}
    Given the name of an author,
    gets all records by this author from the database,
    and passes them on to the follow-up command.

`get journal <journal name> [<limit>]` --> {records}
    Given the name of a journal,
    gets all articles published therein from the database,
    and passes them on to the follow-up command.

`get publisher <journal name> [<limit>]` --> {records}
    Given the name of a publisher,
    gets all books with this publisher from the database,
    and passes them on to the follow-up command.


## Follow-up sub-queries (the receiving-producing kind)

This section presents commands which must appear after
a "producing" command.

{records} --> `tag <tag name> [create [<color>]]` --> {records}
    Tags all records that it receives with the specified tag.
    If the tag with the given name does not exist,
    the creation of the tag has to be confirmed.
    This confirmation can be provided when invoking the
    command with the 'create' option.
    This option can take a hexadecimal color code
    (e.g. D19F93) as an extra option.
    If a tag carries a color code, it will be displayed
    with that color.
    The command passes on all received records.

{records} --> `untag <tag name> [yes]` --> {records}
    Removes the specified tag from all received records.
    If after this operation no record carries the tag
    the command asks if the tag should be deleted.
    Confirmation for deleting the tag in such a case
    can be provided when invoking the command with
    'yes' option.
    The command passes on all received records.


## Terminal follow-up sub-queries (the receiving-closed kind)

This section presents commands which must appear after
a "producing" command and must be the last command
of a pipeline.

{records} --> `show [verbose]`
    Prints the key and the title of every received record.
    If multiple records have been received,
    the command prints a short summary.
    If the 'verbose' option is given, further information
    (tags, journal / publisher, ...) is included.

{records} --> `open [folder]`
    Opens the PDF file named '<title>.pdf' in the
    folder of every received record.
    If such a file does not exist or the 'folder' option
    is provided, the record folder itself is opened.
    The commands used for opening PDF files and folders,
    can be specified in the configuration file.

{records} --> `export bibtex [< path to bib file > [overwrite]]`
    Converts all received records to the BibTeX format.
    If a path to a '*.bib' file is provided,
    the output will be written in that file.
    If the file already exists, the command asks
    if it should be overwritten. This confirmation can be provided
    when invoking the command with the 'overwrite' option.
    If no path is given, the BibTeX output will be
    printed to the command line.

{records} --> `delete [yes] [dangling]`
    Deletes all received records from the database.
    The record folder will also be deleted.
    A command for deleting the folder can be specified
    in the configuration file.    
    If the 'yes' option is not provided,
    the command will ask for confirmation
    for each record individually.
    If eg. a tag or a journal remain dangling
    after deleting the record, the user is asked
    if the dangling database entry should also be
    deleted. Confirmation for deleting dangling
    database entries can be provided when invoking
    the command with the 'dangling' option.


## Examples

- Add an article and move a PDF file to the record folder:  
  `add article ~/Downloads/some_article.pdf`
  
- Open the record folder of the record with the key '2012GregoryStone':  
  `get key 2012GregoryStone : open folder`

- Show information about the five most-recently added records:  
  `get all 5 : show`

- Open the PDF files of at most three records  
  which were tagged 'read-me' recently and remove this tag:  
  `get tag read-me 3 : untag read-me : open`

- Delete (without further confirmation) all records which are tagged 'trash':  
  `get tag trash : delete yes`

- Export the entire collection to a BibTeX file:  
  `get all : export bibtex ~/Desktop/references.bib overwrite`


# Configuration

A configuration file '~/.bibliophant' is required for the application to work.
If the file does not exist, a "configuration wizard" will be invoked automatically.

The following options are required:
- a list of collection folders
- a command for opening PDF files
- a command for opening record folders
- a command for deleting record folders


A configuration file (~/.bibliophant) might then look like this:
{
    "collections": ["~/my/default/collection", "~/my/other/collection"],
    "open_pdf": "open",
    "open_folder": "open",
    "delete_folder": "rmtrash"
}

Note that the JSON format is very picky about commas.
"""
