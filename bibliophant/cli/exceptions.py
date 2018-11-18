"""this module defines custom exceptions"""


class CmdAbortError(Exception):
    """Raising this stops further processing of a command
    and causes the session to be rolled back.

    Before raising this, the user should be informed about the problem!
    """

    pass
