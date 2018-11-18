"""tag command group"""

import click

from bibliophant.models import Tag

from ..exceptions import CmdAbortError


def cmd_tag_list(session, words, results, root):
    """list tags"""

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

    tags = session.query(Tag).order_by(Tag.name.asc()).limit(limit)

    output = ""
    for tag in tags:
        output += str(tag) + "\n"

    click.echo_via_pager(output)

    return tags


tag_subcommands = {"list": cmd_tag_list}
