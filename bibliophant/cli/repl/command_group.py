"""a command that groups other commands"""

__all__ = ["CommandGroup"]


from typing import Dict, List, Tuple, Optional

import click

from prompt_toolkit.completion import Completion

from .command import Command
from .exceptions import QueryAbortError


class CommandGroup(Command):
    """a command that groups other commands
    Usually the (root) command of the REPL will be a CommandGroup.
    """

    def __init__(self, name: str, parent_name: Optional[str] = None):
        super().__init__(name, parent_name)
        self.sub_commands = {}

    def execute(self, arguments, session, root, result=None):
        """Process arguments looking for sub-commands.
        Note that 'result' can be used for chaining sub-commands.
        """

        # split query according to sub-commands
        sub_queries = break_up_query(self.sub_commands, arguments)

        # execute each sub-command
        # feeding it the result of the preceeding command (if any)
        for command, arguments in sub_queries:
            result = command.execute(arguments, session, root, result)

    def add(self, name: str):
        """class decorator for adding a Command as a member of a CommandGroup
        This decorator is syntactic sugar for instantiating the decorated
        Command class and adding it to the group's sub_commands
        dictionary with the key given by the argument name.
        """

        def class_decorator(Cls):
            assert issubclass(Cls, Command)
            self.sub_commands[name] = Cls(name=name, parent_name=self.name)

        return class_decorator

    def get_completions(self, document, complete_event):
        """TODO"""
        if is_place_for_completions(document.text, self.name):
            yield from (Completion(name) for name in self.sub_commands)
            if self.name == "":
                yield Completion("exit")
        else:
            pass

        # try:
        #     first_word = document.text.split(maxsplit=1)[0]
        # except IndexError:
        #     first_word = None

        # if first_word and first_word in self.sub_commands:
        #     yield from self.sub_commands[first_word].get_completions(
        #         document, complete_event
        #     )
        # else:
        #     pos = document.cursor_position
        #     for name in self.sub_commands:
        #         yield Completion(name, start_position=-pos)
        #     if self.name == "":  # root command
        #         yield Completion("exit", start_position=-pos)


def is_place_for_completions(text: str, name: str):
    if name == "" and text == "":
        return True

    if text[-len(name) + 1 :] == name + " ":
        return True

    return False


def break_up_query(
    commands: Dict[str, Command], text: str
) -> List[Tuple[Command, str]]:
    """break up a (sub-)query into parts
    Each sub-query is a tuple of a Command and its unprocessed arguments.
    """
    sub_queries = []
    while True:
        # work from right to left
        # get highest index at which a command name starts
        index = get_index_of_command(commands, text)

        # if no command name is found stop
        if index is None:
            break

        # extract the rightmost part which belongs to the last command
        sub_query = text[index:].rstrip()
        # split of the first word which is the command name itself
        parts = sub_query.split(maxsplit=1)
        if len(parts) == 2:
            name, args = parts
        else:
            name = parts[0]
            args = ""

        # on success add the command which was found together with
        # all unprocessed arguments to the list
        sub_queries.append((commands[name], args))

        # cut off the part that was just processed
        text = text[:index]

    # check the remainder
    text = text.strip()
    if text:
        click.secho(f"Error: '{text}' is not a command", err=True, fg="red")
        raise QueryAbortError

    # since we worked from right to left, the list must be reversed
    sub_queries.reverse()

    return sub_queries


def get_index_of_command(commands: Dict[str, Command], text: str) -> Optional[int]:
    """Returns the highest index i such that
    text[i:] is a sub-query,
    i.e. a string that starts with a command's name.
    """
    length = len(text)
    indices = []
    for name in commands:
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
