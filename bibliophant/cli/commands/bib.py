"""This module defines the root command of the application."""

from ..repl import CommandGroup, Command

bib = CommandGroup()


@bib.add("help")
class Help(Command):
    def execute(self, arguments, session, root, result=None):
        print("Help")

    def get_completions(self, document, complete_event):
        yield None
