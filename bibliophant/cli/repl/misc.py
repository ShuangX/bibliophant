"""This module defines some helper functions"""

__all__ = ["ask_yes_no", "ask_for_folder"]


from pathlib import Path

from prompt_toolkit import prompt

from .exceptions import print_error


def ask_yes_no(question: str) -> bool:
    """Ask the user a [y/N] question."""
    while True:
        answer = prompt(question + " [y/N]: ").strip().lower()
        if answer == "y":
            return True
        elif answer == "n":
            return False


def ask_for_folder(question: str) -> Path:
    """Ask the user about an existing folder."""
    while True:
        answer = prompt(question)
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
                return path
