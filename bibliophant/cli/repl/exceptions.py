"""this module defines custom exceptions and functions for error handling"""

__all__ = ["QueryAbortError", "abort_query"]


# TODO switch from click to prompt toolkit printing function
import click


class QueryAbortError(Exception):
    """Raising this stops further processing of a query
    and causes the session to be rolled back.

    Before raising this, the user should be informed about the problem!
    """

    pass


def abort_query(message: str):
    """Print an error message and stop the execution of the current query."""
    click.secho(f"Error: {message}", err=True, fg="red")
    raise QueryAbortError
