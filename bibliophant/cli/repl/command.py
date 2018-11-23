"""abstract base class for a command"""

__all__ = ["Command"]

from typing import Optional
from abc import ABCMeta, abstractmethod
from pathlib import Path

from prompt_toolkit.completion import Completer


class Command(Completer, metaclass=ABCMeta):
    """abstract base class for a command

    Each command must implement the abstract methods
    'get_completions(self, document, complete_event)' and
    'execute(self, arguments: str, session, root: Path, result=None)'.
    """

    def __init__(self, name: str, parent_name: Optional[str] = None):
        # name of the command
        # put the empty string (""), if it is the root command of the REPL
        self.name = name

        # name of the CommandGroup this Command belongs to
        # put None, if the command does not belong to a CommandGroup
        self.parent_name = parent_name

    @abstractmethod
    def execute(self, arguments: str, session, root: Path, result=None):
        """define what happens when the command executes
        Parameters:
        -----------
        arguments: the unprocessed arguments specified by the user
        session: sqlalchemy session
        root: path to the collection's root folder
        result: can any result from a previously executed command (command chaining)
        """
        pass
