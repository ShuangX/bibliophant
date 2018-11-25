"""this module defines custom exceptions and functions for error handling"""

__all__ = ["QueryAbortError"]


class QueryAbortError(Exception):
    """Raising this stops further processing of a query
    and causes the session to be rolled back.
    Add an error message for the user as an argument.
    """

    pass
