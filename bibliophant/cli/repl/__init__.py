"""This package contains the logic of the interactive user interface
but no definitions of the actual commands.
"""

# main class of the user interface
from .repl import Repl

# abstract base class defining what a command is
from .command import Command

# definition of a command that groups other commands
from .command_group import CommandGroup

# exception which stops the execution of a query
from .exceptions import QueryAbortError
