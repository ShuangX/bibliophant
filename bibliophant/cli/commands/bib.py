"""This module defines the root command of the application."""

from pathlib import Path
from subprocess import call

from prompt_toolkit.completion import Completion

from ..repl import CommandChain, Command


bib = CommandChain(name="")  # root command -> empty string


@bib.add("exit", "closed-closed")
class Exit(Command):
    def execute(self, arguments, session, config, result=None):
        print("Ciao!")
        raise EOFError


@bib.add("ipython", "closed-closed")
class IPython(Command):
    def execute(self, arguments, session, config, result=None):
        bibliophant_path = Path(__file__).parent.parent.parent
        call(
            [
                "ipython",
                "-i",
                bibliophant_path / "start_shell.py",
                "--",
                config["root"],
                bibliophant_path.parent,
            ]
        )


@bib.add("edit", "closed-closed")
class Edit(Command):
    def execute(self, arguments, session, config, result=None):
        # TODO
        print("better spin up the editor soon ...")

    def get_completions(self, document, complete_event):
        # TODO
        return []


@bib.add("add", "closed-producing")
class AddRecord(Command):
    def execute(self, arguments, session, config, result=None):
        # TODO
        print("better spin up the editor soon to add stuff ...")

    def get_completions(self, document, complete_event):
        # TODO
        return []
