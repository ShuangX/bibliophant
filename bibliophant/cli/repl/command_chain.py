"""A command that allows chaining other commands
This command makes sense is particular as a root command.

The individual parts of a command chain are separated by " : ".
Here the colon takes a similar meaning as the shell's pipe operator " | ".
Note that the spaces to the left and right of the colon are obligatory
to make the command work.

Sub-commands are divided into four groups
according to their behaviour at either boundary:
- left end:
    - closed: no input is accepted from a previous command
    - receiving: execution depends on input from the previous command

- right end:
    - closed: no output is produced for a follow-up command
    - producing: output is produced and may be consumed by a follow-up command
"""

__all__ = ["CommandChain"]


from typing import Dict, List, Tuple, Optional

import click

from prompt_toolkit.completion import Completion

from .command import Command
from .exceptions import QueryAbortError


class CommandChain(Command):
    """a command that allows chaining other commands"""

    def __init__(self, name: str, parent_name: Optional[str] = None):
        super().__init__(name, parent_name)

        # These commands must run solo.
        self.closed_closed_sub_commands = {}

        # These commands must run first
        # and may be followed by others.
        self.closed_producing_sub_commands = {}

        # These must run as follow-up commands.
        self.receiving_producing_sub_commands = {}

        # These must run as follow-up commands
        # but they may not be followed by any other commands.
        self.receiving_closed_sub_commands = {}

    def execute(self, arguments, session, root, result=None):
        """Split query into chain-segments and delegate the execution."""

        chain_segments = arguments.split(" : ")

        for i, segment in enumerate(chain_segments):

            # split the segment further into first word and rest
            parts = segment.split(maxsplit=1)
            if len(parts) == 2:
                first, rest = parts
            else:
                first = parts[0]
                rest = None

            # check the four different cases ...

            # closed - closed case
            # These commands must run solo.
            if first in self.closed_closed_sub_commands:
                if i == 0 and len(chain_segments) == 1:
                    print(f"closed - closed: {first} ({rest})")
                    chain_segments[i] = (self.closed_closed_sub_commands[first], rest)
                else:
                    click.secho(
                        f"Error: '{first} makes sense only as a solo-command.",
                        err=True,
                        fg="red",
                    )
                    raise QueryAbortError

            # closed - producing case
            # These commands must run first
            # and may be followed by others.
            elif first in self.closed_producing_sub_commands:
                if i == 0:
                    print(f"closed - producing: {first} ({rest})")
                    chain_segments[i] = (
                        self.closed_producing_sub_commands[first],
                        rest,
                    )
                else:
                    click.secho(
                        f"Error: '{first}' makes sense only as the first command of a chain.",
                        err=True,
                        fg="red",
                    )
                    raise QueryAbortError

            # receiving - producing case
            # These must run as follow-up commands.
            elif first in self.receiving_producing_sub_commands:
                if i > 0:
                    print(f"receiving - producing: {first} ({rest})")
                    chain_segments[i] = (
                        self.receiving_producing_sub_commands[first],
                        rest,
                    )
                else:
                    click.secho(
                        f"Error: '{first}' makes sense only as a follow-up command.",
                        err=True,
                        fg="red",
                    )
                    raise QueryAbortError

            ## receiving - closed case
            # These must run as follow-up commands
            # but they may not be followed by any other commands.
            elif first in self.receiving_closed_sub_commands:
                if i > 0 and i == len(chain_segments) - 1:
                    print(f"receiving - closed: {first} ({rest})")
                    chain_segments[i] = (
                        self.receiving_closed_sub_commands[first],
                        rest,
                    )
                else:
                    click.secho(
                        f"Error: '{first}' makes sense only as a terminal follow-up command.",
                        err=True,
                        fg="red",
                    )
                    raise QueryAbortError

            else:
                click.secho(f"Error: '{first}' is not a command.", err=True, fg="red")
                raise QueryAbortError

        # delegate execution of each segment
        for command, arguments in chain_segments:
            result = command.execute(arguments, session, root, result)

    def add(self, name: str):
        """class decorator for adding a Command as a member of a CommandGroup
        This decorator is syntactic sugar for instantiating the decorated
        Command class and adding it to the group's sub_commands
        dictionary with the key given by the argument name.
        """

        def class_decorator(Cls):
            assert issubclass(Cls, Command)
            self.sub_commands[name] = Cls(name=name, parent_name=self.name)

        return class_decorator

    def get_completions(self, document, complete_event):
        """TODO"""
        yield None
