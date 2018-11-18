"""record command group"""

import click

from bibliophant.models import Record

from ..exceptions import CmdAbortError


def cmd_record_list(session, words, results, root):
    """list records"""

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

    records = session.query(Record).order_by(Record.key.asc()).limit(limit)

    output = ""
    for record in records:
        output += record.key + "\n"
        output += record.title + "\n\n"

    click.echo_via_pager(output)

    return records


record_subcommands = {"list": cmd_record_list}
