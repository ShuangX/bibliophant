"""This module defines a base class for all classes which map to SQL tables.
It further defines a mixin class which specifies created_date and
modified_date fields.
"""

__all__ = []

from contextlib import contextmanager

from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import DateTime
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///library.db")


class BaseMixin:
    @declared_attr
    def created_date(cls):
        return Column(DateTime, default=func.now())

    @declared_attr
    def modified_date(cls):
        return Column(DateTime, default=func.now(), onupdate=func.now())


ModelBase = declarative_base(cls=BaseMixin)


_SessionFactory = sessionmaker(bind=engine)


def session_factory():
    ModelBase.metadata.create_all(engine)
    return _SessionFactory()


@contextmanager
def db():
    """Provides a transactional scope around a series of operations."""
    session = session_factory()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
