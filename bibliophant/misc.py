__all__ = ["key_generator"]

from typing import Dict, List


def key_generator(year: int, authors: List[Dict[str, str]]) -> str:
    """Creates a key for a (new) record."""
    key = str(year)
    for author in authors:
        key += author["last"]
    return key.replace(" ", "")
