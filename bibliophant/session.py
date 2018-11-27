"""This module defines a function resolve_root, which should be used to
get a Path object representing the root folder of a collection.
It also defines a function start_engine, which should be called with the
root Path to open the database file.
Afterwards, the context manager session_scope can be used to work
with the database.

example:
> from session import *
> from models import *
> root = resolve_root("./my_collection")
> start_engine(root)

after having done this you can always use session_scope to talk to the db:
> with session_scope() as s:
>     records = s.query(Record).all()
"""

__all__ = ["resolve_root", "start_engine", "session_scope"]


from pathlib import Path
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def resolve_root(root_folder: str) -> Path:
    """Resolves the root folder of a collection.
    Raises FileNotFoundError if the root_folder cannot be resolved.
    Raises ValueError if it is not a folder.
    """
    try:
        root = Path(root_folder).expanduser().resolve(strict=True)
    except FileNotFoundError:
        raise FileNotFoundError(f"the path {root_folder} could not be resolved.")

    if not root.is_dir():
        raise ValueError(f"the path {root_folder} is not a folder")

    return root


_session_factory = sessionmaker()


def start_engine(root: Path, create_db: bool = False):
    """Creates an engine for the collection's database.
    The engine is then bound to the session factory,
    which can be used via the context manager 'session_scope'.
    Raises FileNotFoundError if root does not contain a database file.
    If create_db is set, no error is raised and the database file is
    initialized instead.
    """
    sqlite_file = root / "bibliophant.db"
    if sqlite_file.is_file():
        engine = create_engine("sqlite:///" + str(sqlite_file))
    else:
        if create_db:
            engine = create_engine("sqlite:///" + str(sqlite_file))
            from .models.base import init_database

            init_database(engine)
        else:
            raise FileNotFoundError(
                f"the path {root} does not contain a file bibliophant.db"
            )
    _session_factory.configure(bind=engine)


@contextmanager
def session_scope() -> "Iterator[sqlalchemy.orm.session.Session]":
    """Provide a transactional scope around a series of operations."""
    session = _session_factory()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
