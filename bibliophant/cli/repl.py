"""interactive user interface for bibliophant"""

from pathlib import Path

import click

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import DynamicCompleter

from .completer import BibCompleter
from .exceptions import CmdAbortError
from .commands import command_groups
from ..session import session_scope


class Repl:
    """interactive user interface"""

    def __init__(self, root: Path):
        self.root = root
        self.completer = BibCompleter()

    def run(self):
        """run the REPL"""

        session = PromptSession(
            completer=DynamicCompleter(lambda: self.completer),
            complete_while_typing=True,
        )

        prompt = f"{self.root.name}> "

        try:
            while True:
                try:
                    text = session.prompt(prompt)
                except KeyboardInterrupt:
                    continue

                self.execute_command(text)

        except EOFError:
            pass

    def execute_command(self, text: str):
        """deal with user input"""
        try:
            with session_scope() as session:
                commands = text.split("|")
                results = None  # used for chaining commands
                for command_text in commands:
                    words = command_text.split()
                    if not words:
                        return
                    words.reverse()
                    group_name = words.pop()
                    if group_name == "exit":
                        raise EOFError
                    elif group_name in command_groups:
                        if words:
                            subcommand_name = words.pop()
                            subcommands = command_groups[group_name]
                            if subcommand_name in subcommands:
                                subcommand = subcommands[subcommand_name]
                                results = subcommand(session, words, results, self.root)
                            else:
                                click.secho(
                                    f"Error: unknown command '{group_name} {subcommand_name}'",
                                    err=True,
                                    fg="red",
                                )
                                raise CmdAbortError
                        else:
                            click.secho(
                                f"Error: {group_name} is missing subcommand",
                                err=True,
                                fg="red",
                            )
                            raise CmdAbortError
                    else:
                        click.secho(
                            f"Error: unknown command '{group_name}'", err=True, fg="red"
                        )
                        raise CmdAbortError
        except CmdAbortError:
            pass
