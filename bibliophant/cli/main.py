"""this is the main module of the CLI user interface of bibliophant"""
__all__ = ["bib"]

import sys
import json
from subprocess import call

import click

from ..session import resolve_root, start_engine, session_scope
from .repl import Repl

from .commands.bib import bib as root_command

# these imports are for click subcommands
from ..models import Record, Author
from ..json_io import record_from_dict, store_record
from ..exporters import bibtex
from ..importers import arxiv, crossref
from ..db_shortcuts import is_key_available


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
        # store root and then continue with click subcommand
        ctx.obj = Collection(root)


# TODO functions below are drafts only


@bib.command()
@click.pass_obj
def show_root(collection):
    """print the collection's root folder"""
    click.echo(collection.root)


@bib.command()
def list_records():
    """list records (key and title)"""
    with session_scope() as session:
        for record in sorted(session.query(Record).all(), key=lambda r: r.key):
            click.echo(record.key)
            click.echo(record.title)
            click.echo("")


@bib.command()
def list_authors():
    """list authors and how many records they have"""
    with session_scope() as session:
        for author in sorted(session.query(Author).all(), key=lambda a: a.last):
            click.echo(f"{len(author.records) :>2} {str(author)}")


@bib.command()
@click.argument("last_name", type=click.STRING)
def list_records_by_last(last_name):
    """list records that have an author with given last name"""
    with session_scope() as session:
        for author in session.query(Author).filter(Author.last == last_name):
            click.echo(author)
            for record in author.records:
                click.echo("\t" + record.key)
                click.echo("\t" + record.title)
                click.echo("")


@bib.command()
@click.argument("key", type=click.STRING)
def show_record(key):
    """show record's data"""
    with session_scope() as session:
        results = session.query(Record).filter(Record.key == key).all()
        if len(results) == 1:
            record = results[0]
            click.echo(json.dumps(record.to_dict(), indent=2))
        else:
            click.secho(
                f"Error: there were {len(results)} results found", err=True, fg="red"
            )
            sys.exit(-1)


@bib.command()
@click.pass_obj
@click.argument("key", type=click.STRING)
def open_record(collection, key):
    """open record (folder or PDF file)"""
    with session_scope() as session:
        if is_key_available(session, key):
            click.secho(f"Error: the key does not exist", err=True, fg="red")
            sys.exit(-1)
    try:
        path = collection.root / key
        files = list(path.glob("*.pdf"))
        if files:
            first_file = next().as_uri()
            call(["open", first_file])
        else:
            call(["open", path])
    except Exception as exception:
        click.secho("Error: " + str(exception), err=True, fg="red")
        sys.exit(-1)


@bib.command()
@click.argument("key", type=click.STRING)  # , required=False
def record_to_bibtex(key):  # =None
    """export record with given key as BibTeX"""
    with session_scope() as session:
        results = session.query(Record).filter(Record.key == key).all()
        assert len(results) == 1
        record = results[0]
        result = bibtex.record_to_bibtex(record)
    click.echo(result)


@bib.command()
@click.pass_obj
@click.option(
    "-o", "--overwrite", is_flag=True, help="Overwrite the file if it already exists."
)
@click.option(
    "-p", "--path", type=click.Path(), help="Specify the path to the output file."
)
def collection_to_bibfile(collection, overwrite, path=None):
    """export all records to a BibTeX file (by default references.bib inside root)"""
    if path is None:
        path = collection.root / "references.bib"
    try:
        with session_scope() as session:
            bibtex.collection_to_bibfile(
                session=session, full_path=path, overwrite=overwrite
            )
    except Exception as exception:
        click.secho("Error: " + str(exception), err=True, fg="red")
        sys.exit(-1)


@bib.command()
@click.pass_obj
@click.argument("arxiv_id", type=click.STRING)
def import_arxiv(collection, arxiv_id):
    """import a record (incl. PDF) from the arXiv"""
    try:
        record = arxiv.arxiv_id_to_record(arxiv_id)
    except Exception as exception:
        click.secho(
            "Error: the bibliographic data could not be downloaded from the arXiv",
            err=True,
            fg="red",
        )
        click.secho(exception, err=True, fg="red")
        sys.exit(-1)

    click.echo("the following data was aquired:")
    click.echo(json.dumps(record, indent=2))
    click.confirm("Do you want to continue with this data?", abort=True)

    try:
        record = record_from_dict(record)
    except Exception as exception:
        click.secho(
            "Error: there is something wrong with the bibliographic data",
            err=True,
            fg="red",
        )
        click.secho(exception, err=True, fg="red")
        sys.exit(-1)

    with session_scope() as session:
        click.echo("storing record ...")
        try:
            if is_key_available(session, record.key):
                session.add(record)
                store_record(record, collection.root)
            else:
                raise FileExistsError("they key is already used")
        except Exception as exception:
            click.secho("Error: the record could not be stored.", err=True, fg="red")
            click.secho(exception, err=True, fg="red")
            sys.exit(-1)

        click.echo("downloading PDF ...")
        try:
            arxiv.download_arxiv_eprint(record, collection.root)
        except Exception as exception:
            click.secho(
                "Error: the PDF could not be fetched and stored to disk.",
                err=True,
                fg="red",
            )
            click.secho(exception, err=True, fg="red")
            sys.exit(-1)


@bib.command()
@click.pass_obj
@click.argument("doi", type=click.STRING)
def import_doi(collection, doi):
    """import a record from crossref"""
    try:
        record = crossref.doi_to_record(doi)
    except Exception as exception:
        click.secho(
            "Error: the bibliographic data could not be downloaded from crossref",
            err=True,
            fg="red",
        )
        click.secho(exception, err=True, fg="red")
        sys.exit(-1)

    click.echo("the following data was aquired:")
    click.echo(json.dumps(record, indent=2))
    click.confirm("Do you want to continue with this data?", abort=True)

    try:
        record = record_from_dict(record)
        key = record.key
    except Exception as exception:
        click.secho(
            "Error: there is something wrong with the bibliographic data",
            err=True,
            fg="red",
        )
        click.secho(exception, err=True, fg="red")
        sys.exit(-1)

    with session_scope() as session:
        click.echo("storing record ...")
        try:
            if is_key_available(session, record.key):
                session.add(record)
                store_record(record, collection.root)
            else:
                raise FileExistsError("they key is already used")
        except Exception as exception:
            click.secho("Error: the record could not be stored.", err=True, fg="red")
            click.secho(exception, err=True, fg="red")
            sys.exit(-1)

    open_record(collection, key)
