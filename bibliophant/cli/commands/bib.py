"""This module defines the root command of the application."""

from typing import Optional
from pathlib import Path
from subprocess import call

from prompt_toolkit.completion import Completion

from ..repl import CommandChain, CommandGroup, Command


bib = CommandChain(name="")  # root command -> empty string


@bib.add("help", "closed-closed")
class Help(Command):
    def execute(self, arguments, session, root, result=None):
        print("Help message ...")

    def get_completions(self, document, complete_event):
        pass


@bib.add("exit", "closed-closed")
class Exit(Command):
    def execute(self, arguments, session, root, result=None):
        print("Goodbye!")
        raise EOFError

    def get_completions(self, document, complete_event):
        pass


@bib.add("ipython", "closed-closed")
class IPython(Command):
    def execute(self, arguments, session, root, result=None):
        bibliophant_path = Path(__file__).parent.parent.parent
        call(
            [
                "ipython",
                "-i",
                bibliophant_path / "start_shell.py",
                "--",
                root,
                bibliophant_path.parent,
            ]
        )

    def get_completions(self, document, complete_event):
        pass


@bib.add("edit", "closed-closed")
class IPython(Command):
    def execute(self, arguments, session, root, result=None):
        print("better spin up the editor soon ...")

    def get_completions(self, document, complete_event):
        pass


@bib.add("add", "closed-producing")
class IPython(Command):
    def execute(self, arguments, session, root, result=None):
        print("better spin up the editor soon to add stuff ...")

    def get_completions(self, document, complete_event):
        pass


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
