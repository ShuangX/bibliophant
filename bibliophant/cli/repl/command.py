"""abstract base class for a command"""

__all__ = ["Command"]


from abc import ABCMeta, abstractmethod
from pathlib import Path

from prompt_toolkit.completion import Completer


class Command(Completer, metaclass=ABCMeta):
    """abstract base class for a command

    Each command must implement the abstract methods
    'get_completions(self, document, complete_event)' and
    'execute(self, arguments: str, session, root: Path, result=None)'.
    """

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
