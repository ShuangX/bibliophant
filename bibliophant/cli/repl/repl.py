"""interactive user interface (for bibliophant)

The implementation should be more or less generic.

With regard to the database, every query is embedded
into its own transactional scope (session_scope context manager).
"""

__all__ = ["Repl"]


from pathlib import Path

from prompt_toolkit import PromptSession

from bibliophant.session import session_scope

from .command import Command
from .exceptions import QueryAbortError, print_error


class Repl:
    """interactive user interface"""

    def __init__(self, command: Command, root: Path):
        assert isinstance(command, Command)
        self.command = command
        self.root = root

    def run(self):
        """run the REPL"""

        prompt_session = PromptSession(
            completer=self.command,
            # complete_while_typing=True,
            vi_mode=True,
        )

        prompt = f"{self.root.name}> "

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
                            self.command.execute(query, session, self.root)

                    # If a command raised QueryAbortError it must have
                    # informed the user about the problem.
                    # The session_scope context manager will roll back the session.
                    except QueryAbortError as error:
                        print_error(error)

        # On EOF (Ctrl-D), exit the REPL
        except EOFError:
            pass
