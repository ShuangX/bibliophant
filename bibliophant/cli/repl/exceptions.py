"""this module defines custom exceptions"""


class QueryAbortError(Exception):
    """Raising this stops further processing of a query
    and causes the session to be rolled back.

    Before raising this, the user should be informed about the problem!
    """

    pass
