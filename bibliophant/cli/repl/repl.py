"""interactive user interface (for bibliophant)

The implementation should be more or less generic.

With regard to the database, every query is embedded
into its own transactional scope (session_scope context manager).
"""

__all__ = ["Repl"]


from typing import Dict, Optional
import sys

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

from bibliophant.session import session_scope

from .command import Command
from .exceptions import QueryAbortError, print_error


class Repl:
    """interactive user interface"""

    def __init__(self, root_command: Command, config: Dict):
        assert isinstance(root_command, Command)
        self.root_command = root_command
        self.config = config

    def run(self):
        """run the REPL"""

        prompt_session = PromptSession(
            history=get_history(self.config),
            completer=self.root_command,
            # complete_while_typing=True,
            vi_mode=True,
        )

        prompt = f"{self.config['root'].name}> "

        try:
            while True:
                try:
                    query = prompt_session.prompt(prompt)
                # On Ctrl-C, trash the current query but continue running
                except KeyboardInterrupt:
                    continue

                # If the user has typed anything, process it
                if query.strip():
                    try:
                        # each query has its own transactional scope
                        with session_scope() as session:
                            self.root_command.execute(query, session, self.config)

                    # If a command raised QueryAbortError it must have
                    # informed the user about the problem.
                    # The session_scope context manager will roll back the session.
                    except QueryAbortError as error:
                        print_error(error)

        # On EOF (Ctrl-D), exit the REPL
        except EOFError:
            pass


def get_history(config) -> Optional[FileHistory]:
    """Returns a FileHistory object,
    if history is enabled in the configuration file.
    Otherwise returns None.
    """

    # parse the value in the configuration file

    try:
        enabled = config["history"]
    except KeyError:
        enabled = False

    if not isinstance(enabled, bool):
        print_error(
            "The history field in the configuration file must be a boolean value."
        )
        print("Please put 'history: true' or 'history: false'.")
        sys.exit(-1)

    # return the according value

    if enabled:
        history_file = config["root"] / ".cli_history"
        return FileHistory(history_file)

    return None
