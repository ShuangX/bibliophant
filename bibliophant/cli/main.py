"""This is the entry-point for the command-line user interface of bibliophant."""

__all__ = ["bib"]


import argparse
import json
import sys
from pathlib import Path

from ..session import resolve_root, start_engine, session_scope
from .repl import Repl, QueryAbortError, print_error
from .repl.misc import ask_yes_no
from .commands import root_command
from .config_wizard import config_wizard


def bib():
    """bibliophant is a tool for managing bibliographies and PDF documents"""

    # read the configuration file

    config_file = Path.home() / ".bibliophant"

    try:
        with open(config_file, "r") as file:
            config = json.load(file)
    except FileNotFoundError:
        print_error(f"The configuration file {config_file} does not exist.")
        if ask_yes_no("Do you want the configuration wizard's help to create it?"):
            config = config_wizard(config_file)
        else:
            sys.exit(-1)

    except json.decoder.JSONDecodeError:
        print_error(
            f'There seems to be a problem with configuration file "{config_file}".\n'
            "Make sure it conforms to the JSON format. For instance, check your commas.\n"
            "You may delete the file and let the configuration wizard recreate it."
        )
        sys.exit(-1)

    # extract the specified collection root folders

    try:
        collections = config["collections"]
        assert isinstance(collections, list)
        assert len(collections) > 0
    except:
        print_error(
            'The configuration file must contain a "collections" field.\n'
            'Example: "collections": ["~/my/default/collection", "~/my/other/collection"]\n'
            "This list must have at least one entry."
        )
        sys.exit(-1)

    # convert strings to Path objects
    collections = [Path(collection) for collection in collections]

    # convert to dict with key = folder name and value = full path
    collections_dict = {collection.name: collection for collection in collections}

    # parse collection argument (-c <name>)

    parser = argparse.ArgumentParser(prog="bib")

    parser.add_argument(
        "-c",
        choices=collections_dict.keys(),
        help=f'selects one of the collections specified in "{config_file}"',
    )

    parser.add_argument(
        "query",
        nargs=argparse.REMAINDER,
        help='Run "bib help" for information on supported queries. If no query is provided, the interactive shell will start.',
    )

    args = parser.parse_args()

    if args.c:
        config["root"] = collections_dict[args.c]
    else:
        config["root"] = collections[0]

    # open the collection's root folder
    try:
        config["root"] = resolve_root(config["root"])
    except:
        print_error(f"The folder \"{config['root']}\" was not found.")
        sys.exit(-1)

    # open database
    try:
        start_engine(config["root"], create_db=True)
    except Exception as error:
        print_error(error)
        sys.exit(-1)

    # run query if provided ; otherwise start interactive shell
    query = " ".join(args.query)
    if query:
        try:
            with session_scope() as session:
                root_command.execute(query, session, config)

        except QueryAbortError as error:
            print_error(error)

    else:
        repl = Repl(root_command=root_command, config=config)
        repl.run()
