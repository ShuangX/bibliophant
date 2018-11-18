"""author command group"""

import click

from bibliophant.models import Author

from ..exceptions import CmdAbortError


def cmd_author_list(session, words, results, root):
    """list authors"""

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

    authors = session.query(Author).order_by(Author.last.asc()).limit(limit)

    output = ""
    for author in authors:
        output += str(author) + "\n"
        if author.email:
            output += author.email + "\n"
        output += "\n"

    click.echo_via_pager(output)

    return authors


author_subcommands = {"list": cmd_author_list}
