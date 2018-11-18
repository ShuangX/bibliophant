"""article command group"""

import click

from bibliophant.models import Article

from ..exceptions import CmdAbortError


def cmd_article_list(session, words, results, root):
    """list articles"""

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

    articles = session.query(Article).order_by(Article.key.asc()).limit(limit)

    output = ""
    for article in articles:
        output += article.key + "\n"
        output += article.title + "\n\n"

    click.echo_via_pager(output)

    return articles


article_subcommands = {"list": cmd_article_list}
