"""This module defines some helper functions"""

__all__ = ["ask_yes_no", "ask_for_folder"]


from pathlib import Path

from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator
from prompt_toolkit.completion import WordCompleter, PathCompleter

from .exceptions import print_error


def _validate_yes_no(text: str) -> bool:
    """validate y/N answers"""
    if text.lower() in ("y", "n"):
        return True
    return False


_yes_no_completer = WordCompleter(["y", "n"])


def ask_yes_no(question: str) -> bool:
    validator = Validator.from_callable(
        _validate_yes_no,
        error_message="Please answer with 'y' or 'n'.",
        move_cursor_to_end=True,
    )

    """Ask the user a [y/N] question."""
    while True:
        answer = (
            prompt(
                question + " [y/N]: ", validator=validator, completer=_yes_no_completer
            )
            .strip()
            .lower()
        )

        if answer == "y":
            return True
        elif answer == "n":
            return False


def _validate_folder(text: str) -> bool:
    """validate path to an existing folder
    The user's home folder is not allowed.
    """
    try:
        path = Path(text).expanduser()
    except:
        return False
    else:
        return path.is_dir() and path != Path.home()


_folder_completer = PathCompleter(only_directories=True, expanduser=True)


def ask_for_folder(question: str) -> Path:
    """Ask the user about an existing folder."""
    validator = Validator.from_callable(
        _validate_folder,
        error_message="Please answer with an existing absolute or relative path.",
        move_cursor_to_end=True,
    )

    while True:
        answer = prompt(question, validator=validator, completer=_folder_completer)
        if answer.strip():
            try:
                path = Path(answer).expanduser().resolve(strict=True)
                assert path.is_dir()
            except FileNotFoundError:
                print_error(f"The path '{answer}' does not exist.")
                print("Check and try again!")
            except RuntimeError:
                print_error(f"Please enter a valid path. Try again!")
            else:
                if path == Path.home():
                    print_error(
                        "Don't use your home folder as the root folder of a collection."
                    )

                else:
                    return path
