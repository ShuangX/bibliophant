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

# from prompt_toolkit.completion import Completion

from .command import Command
from .exceptions import QueryAbortError
from .command_group import CommandGroup


Case = namedtuple("Case", "condition error_message sub_commands")


class CommandChain(Command):
    """a command that allows chaining other commands"""

    def __init__(self, name: str, parent_name: Optional[str] = None):
        super().__init__(name, parent_name)

        # four different command groups / cases
        self.cases = {
            "closed-closed": Case(
                lambda i, n_segments: i == 0 and n_segments == 1,
                "makes sense only as a solo-command",
                {},
            ),
            "closed-producing": Case(
                lambda i, n_segments: i == 0,
                "makes sense only as the first command of a chain",
                {},
            ),
            "receiving-producing": Case(
                lambda i, n_segments: i > 0,
                "makes sense only as a follow-up command",
                {},
            ),
            "receiving-closed": Case(
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
            elif len(parts) == 1:
                first = parts[0]
                rest = ""
            else:
                raise QueryAbortError("empty sub-query")
            # TODO necessary? " : " vs strip

            # check segment against the four different cases
            for case_name, case in self.cases.items():
                if first in case.sub_commands:
                    if case.condition(i, n_segments):
                        print(f"{case_name}: {first} ({rest})")
                        segments[i] = (case.sub_commands[first], rest)
                        break
                    else:
                        raise QueryAbortError(f"'{first} {case.error_message}.")
            else:  # no break was hit
                raise QueryAbortError(f"'{first}' is not a command.")

        # delegate execution of each segment
        for command, arguments in segments:
            result = command.execute(arguments, session, root, result)

    def add(self, command_name: str, case_name: str):
        """Class decorator for adding a Command as a sub-command of the 'case_name' case.
        This decorator is syntactic sugar for instantiating the decorated
        Command class and adding it to the case's sub_commands
        dictionary with the key given by 'command_name'.
        """
        assert case_name in self.cases

        def class_decorator(Cls):
            assert issubclass(Cls, Command)
            self.cases[case_name].sub_commands[command_name] = Cls(
                name=command_name, parent_name=self.name
            )

        return class_decorator

    def add_command_group(self, command_name: str, case_name: str) -> CommandGroup:
        """Add a command group as a sub-command of the 'case_name' case.
        Returns the created group.
        """
        assert case_name in self.cases
        command_group = CommandGroup(name=command_name, parent_name=self.name)
        self.cases[case_name].sub_commands[command_name] = command_group
        return command_group

    def get_completions(self, document, complete_event):
        # TODO
        return []
