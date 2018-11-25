"""A command that allows chaining other commands
This command makes sense is particular as a root command.

The individual parts of a command chain are separated by " : ".
Here the colon takes a similar meaning as the shell's pipe operator " | ".
Note that the spaces to the left and right of the colon are obligatory
to make the command work.

Sub-commands are divided into four groups (Case)
according to their behaviour at either boundary:
- left end:
    - closed: no input is accepted from a previous command
    - receiving: execution depends on input from the previous command

- right end:
    - closed: no output is produced for a follow-up command
    - producing: output is produced and may be consumed by a follow-up command
"""

__all__ = ["CommandChain"]


from typing import Optional
from collections import namedtuple

import click

# from prompt_toolkit.completion import Completion

from .command import Command
from .exceptions import QueryAbortError


Case = namedtuple("Case", "condition error_message sub_commands")


class CommandChain(Command):
    """a command that allows chaining other commands"""

    def __init__(self, name: str, parent_name: Optional[str] = None):
        super().__init__(name, parent_name)

        # four different command groups / cases
        self.cases = {
            "closed_closed": Case(
                lambda i, n_segments: i == 0 and n_segments == 1,
                "makes sense only as a solo-command",
                {},
            ),
            "closed_producing": Case(
                lambda i, n_segments: i == 0,
                "makes sense only as the first command of a chain",
                {},
            ),
            "receiving_producing": Case(
                lambda i, n_segments: i > 0,
                "makes sense only as a follow-up command",
                {},
            ),
            "receiving_closed": Case(
                lambda i, n_segments: i > 0 and i == n_segments - 1,
                "makes sense only as a terminal follow-up command",
                {},
            ),
        }

    def execute(self, arguments, session, root, result=None):
        """Split query into chain-segments and delegate the execution."""

        segments = arguments.split(" : ")
        n_segments = len(segments)

        for i, segment in enumerate(segments):

            # split the segment further into first word and rest
            parts = segment.split(maxsplit=1)
            if len(parts) == 2:
                first, rest = parts
            else:
                first = parts[0]
                rest = None

            # check segment against the four different cases
            for case_name, case in self.cases.items():
                if first in case.sub_commands:
                    if case.condition(i, n_segments):
                        print(f"{case_name}: {first} ({rest})")
                        segments[i] = (case.sub_commands[first], rest)
                        break
                    else:
                        click.secho(
                            f"Error: '{first} {case.error_message}.", err=True, fg="red"
                        )
                        raise QueryAbortError
            else:  # no break was hit
                click.secho(f"Error: '{first}' is not a command.", err=True, fg="red")
                raise QueryAbortError

        # delegate execution of each segment
        for command, arguments in segments:
            result = command.execute(arguments, session, root, result)

    def add(self, command_name: str, case_name: str):
        """class decorator for adding a Command as a sub-command of the 'case_name' case.
        This decorator is syntactic sugar for instantiating the decorated
        Command class and adding it to the case's sub_commands
        dictionary with the key given by 'command_name'.
        """

        def class_decorator(Cls):
            assert issubclass(Cls, Command)
            assert case_name in self.cases
            self.cases[case_name].sub_commands[command_name] = Cls(
                name=command_name, parent_name=self.name
            )

        return class_decorator

    def get_completions(self, document, complete_event):
        """TODO"""
        yield None
