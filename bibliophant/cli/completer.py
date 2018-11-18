"""custom autocompletion for the REPL"""

from prompt_toolkit.completion import Completer, Completion

from .commands import command_groups


group_names = command_groups.keys()


class BibCompleter(Completer):
    """autocompleten for the interactive command line interface"""

    def get_completions(self, document, complete_event):

        text = document.text_before_cursor

        words = text.split()

        return [Completion(group_name, start_position=0) for group_name in group_names]
