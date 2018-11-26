"""This package contains the logic of the interactive user interface
but no definitions of the actual commands.
"""

# abstract base class defining what a command is
from .command import Command

# definition of a command that allows chaining other commands
from .command_chain import CommandChain

# definition of a command that groups other commands
from .command_group import CommandGroup

# raise this to stop the execution of a query; print a user-facing error message
from .exceptions import QueryAbortError, print_error

# main class of the user interface
from .repl import Repl
