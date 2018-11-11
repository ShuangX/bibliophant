__all__ = ["is_key_available"]

from .models import Record


def is_key_available(session: "sqlalchemy.orm.session.Session", key: str) -> bool:
    """Checks if a given key is still available,
    i.e. no other record with this key already exists.
    """
    if session.query(Record).filter(Record.key == key).all():
        return False
    return True
