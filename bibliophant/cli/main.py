"""This is the entry-point for the command-line user interface of bibliophant."""

__all__ = ["bib"]


import sys

import click

from ..session import resolve_root, start_engine, session_scope
from .repl import Repl, QueryAbortError, print_error
from .commands import root_command

# TODO remove click as a dependency?
# can we use argparse for the stuff below?
# how to print through a pager?


@click.command()
@click.option(
    "-r",
    "--root",
    type=click.Path(),
    envvar="BIBLIOPHANT_COLLECTION",
    help="Specify the path to the collection's root folder.",
)
@click.option("--init", is_flag=True, help="Initialize a new collection.")
@click.argument("arguments", nargs=-1)
def bib(init, root=None, arguments=""):
    """bibliophant is a tool for managing bibliographies and PDF documents"""

    if root is None:
        print_error(
            "Please use the environment variable BIBLIOPHANT_COLLECTION "
            "or the -r / --root option "
            "to indicate your collection's root folder."
        )
        sys.exit(-1)

    # open the collection's root folder
    try:
        root = resolve_root(root)
    except:
        print_error("The root folder was not found.")
        sys.exit(-1)

    # open database
    try:
        start_engine(root, create_db=init)
    except Exception as error:
        print_error(error)
        sys.exit(-1)

    # any extra arguments are interpreted as a query
    query = " ".join(arguments)
    if query:
        # shell-mode (execute single query)
        try:
            with session_scope() as session:
                root_command.execute(query, session, root)

        except QueryAbortError as error:
            print_error(error)

    else:
        # interactive user interface (REPL)
        repl = Repl(command=root_command, root=root)
        repl.run()
