"""book command group"""

import click

from bibliophant.models import Book

from .bib import bib
from ..repl import QueryAbortError


def cmd_book_list(session, words, results, root):
    """list books"""

    if results is not None:
        click.secho(
            "Error: command 'article list' cannot be chained to previous command.",
            err=True,
            fg="red",
        )
        raise QueryAbortError

    # default options
    limit = None

    for word in words:
        if word[:6] == "limit=":
            try:
                limit = int(word[6:])
            except:
                click.secho("Error: limit must be an integer", err=True, fg="red")
                raise QueryAbortError
        else:
            click.secho(f"Error: unknown option {word}", err=True, fg="red")
            raise QueryAbortError

    books = session.query(Book).order_by(Book.key.asc()).limit(limit)

    output = ""
    for book in books:
        output += book.key + "\n"
        output += book.title + "\n\n"

    click.echo_via_pager(output)

    return books
