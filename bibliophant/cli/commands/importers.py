"""This module defines the import command group of the application."""

from ..repl import Command
from .bib import bib


import_group = bib.add_command_group("import", "closed-producing")


@import_group.add("doi")
class ImportDoi(Command):
    def execute(self, arguments, session, config, result=None):
        # TODO
        print("import from Crossref and spin up the editor soon ...")

    def get_completions(self, document, complete_event):
        # TODO
        return []


@import_group.add("arxiv")
class ImportArXiv(Command):
    def execute(self, arguments, session, config, result=None):
        # TODO
        print("import from the arXiv and spin up the editor soon ...")

    def get_completions(self, document, complete_event):
        # TODO
        return []


@import_group.add("bib")
class ImportBibliophantRecordFolder(Command):
    def execute(self, arguments, session, config, result=None):
        # TODO
        print("import from record folder and spin up the editor soon ...")

    def get_completions(self, document, complete_event):
        # TODO
        return []
