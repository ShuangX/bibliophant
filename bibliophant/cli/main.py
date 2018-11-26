"""this is the main module of the CLI user interface of bibliophant"""

__all__ = ["bib"]


import sys

import click

from ..session import resolve_root, start_engine
from .repl import Repl
from .commands import root_command


class Collection:
    """context object for the bib command"""

    def __init__(self, root):
        self.root = root


@click.group(invoke_without_command=True)
@click.option(
    "-r",
    "--root",
    type=click.Path(),
    envvar="BIBLIOPHANT_COLLECTION",
    help="Specify the path to the collection's root folder.",
)
@click.option("--init", is_flag=True, help="Initialize a new collection.")
@click.pass_context
def bib(ctx, init, root=None):
    """bibliophant is a tool for managing bibliographies and PDF documents"""
    if root is None:
        click.secho(
            "Error: Please use the environment variable BIBLIOPHANT_COLLECTION "
            "to indicate your collection's root folder "
            "or use the -r / --root option.",
            err=True,
            fg="red",
        )
        sys.exit(-1)

    try:
        root = resolve_root(root)
    except:
        click.secho("Error: the root folder was not found.", err=True, fg="red")
        sys.exit(-1)

    try:
        start_engine(root, create_db=init)
    except Exception as exception:
        click.secho("Error: " + str(exception), err=True, fg="red")
        sys.exit(-1)

    if ctx.invoked_subcommand is None:
        # start interactive user interface
        repl = Repl(command=root_command, root=root)
        repl.run()
    else:
        # store root and then continue with click sub-command
        ctx.obj = Collection(root)
