"""This module defines the 'tag' and 'untag' commands."""

from ..repl import Command
from .bib import bib


@bib.add("tag", "receiving-producing")
class Tag(Command):
    def execute(self, arguments, session, config, result=None):
        # TODO
        print("add a tag to the received records")

    def get_completions(self, document, complete_event):
        # TODO
        return []


@bib.add("untag", "receiving-producing")
class Untag(Command):
    def execute(self, arguments, session, config, result=None):
        # TODO
        print("remove a tag from the received records")

    def get_completions(self, document, complete_event):
        # TODO
        return []
