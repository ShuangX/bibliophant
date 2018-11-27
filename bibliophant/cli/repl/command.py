"""abstract base class for a command"""

__all__ = ["Command"]

from typing import Optional, Dict
from abc import ABCMeta, abstractmethod

from prompt_toolkit.completion import Completer


class Command(Completer, metaclass=ABCMeta):
    """abstract base class for a command"""

    def __init__(self, name: str, parent_name: Optional[str] = None):
        # name of the command
        # put the empty string (""), if it is the root command of the REPL
        self.name = name

        # name of the CommandGroup this Command belongs to
        # put None, if the command does not belong to a CommandGroup
        self.parent_name = parent_name

    @abstractmethod
    def execute(self, arguments: str, session, config: Dict, result=None):
        """define what happens when the command executes
        Parameters:
        -----------
        arguments: the unprocessed arguments specified by the user
        session: sqlalchemy session
        config: configuration dictionary
        result: a result from a previously executed command (command chaining)
        """
        pass

    def get_completions(self, document, complete_event):
        """Overwrite this method to make the command yield auto-completions
        for any of its arguments.
        """
        return []
