"""interactive user interface for bibliophant"""

__all__ = ["Repl"]


from pathlib import Path

from prompt_toolkit import PromptSession

# from prompt_toolkit.completion import DynamicCompleter

from bibliophant.session import session_scope

from .command import Command
from .exceptions import QueryAbortError


class Repl:
    """interactive user interface"""

    def __init__(self, command: Command, root: Path):
        assert isinstance(command, Command)
        self.command = command
        self.root = root

    def run(self):
        """run the REPL"""

        prompt_session = PromptSession(
            # completer=self.command,
            # completer=DynamicCompleter(lambda: self.command),
            # complete_while_typing=True,
            vi_mode=True
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
                    except QueryAbortError:
                        pass

        # On EOF (Ctrl-D), exit the REPL
        except EOFError:
            pass
