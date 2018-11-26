"""this module defines custom exceptions and functions for error handling"""

__all__ = ["QueryAbortError", "print_error"]

from typing import Union

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText


class QueryAbortError(Exception):
    """Raising this stops further processing of a query
    and causes the session to be rolled back.
    Add an error message for the user as an argument.
    """

    pass


def print_error(error: Union[Exception, str]):
    """Turns an Exception or a str into a user-facing error message."""
    message = FormattedText([("#d19393", "Error: "), ("", str(error))])
    print_formatted_text(message)
