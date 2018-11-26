"""This module defines the help command of the application."""

from click import echo_via_pager

from ..repl import Command
from .bib import bib


@bib.add("help", "closed-closed")
class Help(Command):
    def execute(self, arguments, session, root, result=None):
        echo_via_pager(HELP)


HELP = """Bibliophant manual
------------------

# solo queries

`exit`

`help`

`ipython`
    ipython -i start_shell.py -- root

`edit record <record key>`
`edit tag <tag name>`
`edit author <author name>`
`edit publisher <publisher name>`
`edit journal <journal name>`


# at-the-beginning (sub-)queries

`add (article | book) [<path to pdf>]` --> {record}
    editor
    save db
    save json
    if path to pdf:
        move pdf

`import doi <doi> [<path to pdf>]` --> {record}
    editor
    save db
    save json
    if path to pdf:
        move pdf

`import arxiv <arxiv id>` --> {record}
    editor
    save db
    save json
    download eprint

`import bib <path to record folder>` --> {record}
    editor
    save db
    save json
    if files in record folder:
        copy files


# at-the-beginning sub-queries

`get key <record key>` --> {record}
`get title <record title>` --> {record}
`get doi <doi> -->` {record}
`get arxiv <arxiv id>` --> {record}

`get all [<limit>]` --> {records}
`get tag <tag name> [<limit>]` --> {records}
`get author <author name> [<limit>]` --> {records}
`get journal <journal name> [<limit>]` --> {records}
`get publisher <journal name> [<limit>]` --> {records}


# follow-up sub-queries

{records} -> `tag <tag name> [create [<color>]]` --> {records}
    if tag does not exist:
        editor
        save tag
    for record in records:
        add tag to record

{records} --> `untag <tag name> [yes]` --> {records}
    for record in records:
        remove tag from record
    if tag has no records:
        ask if tag should be deleted:
            delete tag


# terminal follow-up sub-queries

{records} --> `show [verbose]`
    if len(records) > 1:
        show how many records, aricles, books
    for record in records:
        show key, title
        if verbose:
            show tags, open_access
            show journal / publisher
            show ...
        show separating blank line(s)
    if length of output > .. lines:
        print through pager
    else:
        print

{records} --> `open [folder]`
    for record in records:
        if folder:
            open record folder
        else:
            try:
                open pdf named title.pdf
            except:
                open record folder

{records} --> `export bibtex [< path to bib file > [overwrite]]`
    for record in records:
        convert record to bibtex
    if bibfile:
        write bibtex to file
    else:
        if len(bibtex) > .. lines:
            print through pager
        else:
            print

{records} --> `delete [yes] [<path to trash>]`
    for record in records:
        if not yes:
            ask for confirmation
        delete db (also check for dangling ...)
        if path to trash:
            move record folder to trash
        else:
            delete record folder (use rmtrash if available)


# some examples

add article ~/Downloads/some_article.pdf
import doi 10.1017/jfm.2012.639 ~/Downloads/foo.pdf
import arXiv 1303.4267 : tag read-me : open
get tag read-me 3 : untag read-me : open
get tag stupid : delete yes
get key 1965Kurokawa : open
get title "fuzzy completed title" : delete
get doi 10.1017/jfm.2012.639 : open folder
get all 5 : open
get author "fuzzy completed author" : show
get all : export bibtex ~/bib/references.bib overwrite
get journal "fuzzy completed journal name" : show verbose

"""
