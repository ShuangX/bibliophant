"""This module defines the root command of the application."""

from typing import Optional

from prompt_toolkit.completion import Completion

from ..repl import CommandGroup, Command


bib = CommandGroup(name="")  # root command -> empty string


@bib.add("help")
class Help(Command):
    def execute(self, arguments, session, root, result=None):
        print("Help")

    def get_completions(self, document, complete_event):
        yield Completion("test help", start_position=0)


@bib.add("test")
class Test(Command):
    def execute(self, arguments, session, root, result=None):
        print("Test")

    def get_completions(self, document, complete_event):
        want_to_see = self.name + " "
        length = len(want_to_see)
        if document.text[-length:] == want_to_see:
            yield Completion("test test", start_position=0)


def get_index_of_command(name: str, text: str) -> Optional[int]:
    """Returns the highest index i such that
    text[i:] is a sub-query,
    i.e. a string that starts with a command's name.
    """
    length = len(text)
    indices = []

    index = text.rfind(name)

    # if command's name was found ...
    if index >= 0:
        # ... make sure it is not part of another word ...
        index_after = index + len(name)
        if index_after >= length or text[index_after] == " ":
            # ... and add its starting position to the list
            indices.append(index)

    # if any command name was found, return the rightmost one
    if indices:
        return max(indices)
    return None
