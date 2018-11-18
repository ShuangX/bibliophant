"""book command group"""

import click

from bibliophant.models import Book

from ..exceptions import CmdAbortError


def cmd_book_list(session, words, results, root):
    """list books"""

    if results is not None:
        click.secho(
            "Error: command 'article list' cannot be chained to previous command.",
            err=True,
            fg="red",
        )
        raise CmdAbortError

    # default options
    limit = None

    for word in words:
        if word[:6] == "limit=":
            try:
                limit = int(word[6:])
            except:
                click.secho("Error: limit must be an integer", err=True, fg="red")
                raise CmdAbortError
        else:
            click.secho(f"Error: unknown option {word}", err=True, fg="red")
            raise CmdAbortError

    books = session.query(Book).order_by(Book.key.asc()).limit(limit)

    output = ""
    for book in books:
        output += book.key + "\n"
        output += book.title + "\n\n"

    click.echo_via_pager(output)

    return books


book_subcommands = {"list": cmd_book_list}
