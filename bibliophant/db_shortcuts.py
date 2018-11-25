"""This module is a collection of helper functions for working with the database."""

__all__ = ["exists_key", "delete_record_and_children", "tag_record", "untag_record"]


from .models import Record, Article, Book, Tag


def exists_key(session: "sqlalchemy.orm.session.Session", key: str) -> bool:
    """Checks if a given key exists."""
    if session.query(Record).filter(Record.key == key).all():
        return True
    return False


def delete_record_and_children(
    session: "sqlalchemy.orm.session.Session", record: Record
):
    """Delete a record and all its dangling children."""
    # delete all dangling authors
    for author in record.authors:
        if len(author.records) == 1:
            assert author.records[0] == record
            session.delete(author)

    # delete all URLs
    for url in record.urls:
        session.delete(url)

    # delete all dangling tags
    for tag in record.tags:
        if len(tag.records) == 1:
            assert tag.records[0] == record
            session.delete(tag)

    if isinstance(record, Article):

        # delete a dangling journal
        if len(record.journal.articles) == 1:
            assert record.journal.articles[0] == record
            session.delete(record.journal)

        # delete the eprint
        if record.eprint:
            session.delete(record.eprint)

    if isinstance(record, Book):

        # delete a dangling publisher
        if len(record.publisher.books) == 1:
            assert record.publisher.books[0] == record
            session.delete(record.publisher)

    # delete the record itself
    session.delete(record)


def tag_record(
    session: "sqlalchemy.orm.session.Session", record: Record, tag_name: str
):
    """Add a tag to a record.
    Raises FileNotFoundError if the tag does not exist in the database.
    """
    # get tag from the database
    tags = session.query(Tag).filter(Tag.name == tag_name).all()
    if not tags:
        raise FileNotFoundError(f"The tag '{tag_name}' does not exist.")
    assert len(tags) == 1
    tag = tags[0]

    # add tag to the record
    record.tags.append(tag)


def untag_record(
    session: "sqlalchemy.orm.session.Session", record: Record, tag_name: str
):
    """Remove a tag from a record.
    If the record does not carry the given tag nothing happens.
    If the no other record carries the tag
    Raises FileNotFoundError if the tag does not exist in the database.
    """
    # get tag from the database
    tags = session.query(Tag).filter(Tag.name == tag_name).all()
    if not tags:
        raise FileNotFoundError(f"The tag '{tag_name}' does not exist.")
    assert len(tags) == 1
    tag = tags[0]

    # remove tag from record
    if tag in record.tags:

        # # delete dangling tag
        # if len(tag.records) == 1:
        #     assert tag.records[0] == record
        #     session.delete(tag)

        record.tags.remove(tag)
