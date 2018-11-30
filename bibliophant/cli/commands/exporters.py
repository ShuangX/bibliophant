"""This module defines the 'export' command group of the application."""

from ..repl import Command
from .bib import bib


export_group = bib.add_command_group("export", "receiving-closed")


@export_group.add("doi")
class BibTeX(Command):
    def execute(self, arguments, session, config, result=None):
        # TODO
        print("export all received records as BibTeX")

    def get_completions(self, document, complete_event):
        # TODO
        return []
