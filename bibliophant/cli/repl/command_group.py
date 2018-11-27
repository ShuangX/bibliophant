"""a command that groups other commands"""

__all__ = ["CommandGroup"]


from typing import Optional

# from prompt_toolkit.completion import Completion

from .command import Command
from .exceptions import QueryAbortError


class CommandGroup(Command):
    """a command that groups other commands"""

    def __init__(self, name: str, parent_name: Optional[str] = None):
        super().__init__(name, parent_name)
        self.sub_commands = {}

    def execute(self, arguments, session, config, result=None):
        """Process arguments looking for sub-commands.
        Note that 'result' can be used for chaining sub-commands.
        """

        # break up arguments into
        # first word (-> sub-command name)
        # and remainder (-> sub-command arguments)
        parts = arguments.split(maxsplit=1)
        if len(parts) == 2:
            first, rest = parts
        elif len(parts) == 1:
            first = parts[0]
            rest = ""
        else:
            raise QueryAbortError(f"'{self.name}' requires a sub-command.")

        # delegate the execution of the sub-command
        if first in self.sub_commands:
            command = self.sub_commands[first]
            return command.execute(rest, session, config, result)
        else:
            raise QueryAbortError(f"'{first}' is not a sub-command of {self.name}.")

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
        # TODO
        return []
