"""This module defines the import command group of the application."""

from ..repl import Command
from .bib import bib


import_group = bib.add_command_group("import", "closed-producing")


@import_group.add("doi")
class ImportDoi(Command):
    def execute(self, arguments, session, root, result=None):
        print("import from Crossref and spin up the editor soon ...")

    def get_completions(self, document, complete_event):
        pass


@import_group.add("arxiv")
class ImportArXiv(Command):
    def execute(self, arguments, session, root, result=None):
        print("import from the arXiv and spin up the editor soon ...")

    def get_completions(self, document, complete_event):
        pass


@import_group.add("bib")
class ImportBibliophantFolder(Command):
    def execute(self, arguments, session, root, result=None):
        print("import from record folder and spin up the editor soon ...")

    def get_completions(self, document, complete_event):
        pass
