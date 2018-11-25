"""This module is a collection of helper functions
which do not involve talking to the the database.
"""

__all__ = ["format_string", "key_generator"]

from typing import Dict, List
from unicodedata import normalize


def format_string(string: str) -> str:
    """Converts a string into compatible unicode normal form (NFKC)
    and removes all excessive whitespace.
    """
    string = normalize("NFKC", string)
    string = " ".join(string.split())
    return string


# BibTeX keys should be ASCII
UNICODE_TO_ASCII = {
    ord("à"): "a",
    ord("á"): "a",
    ord("â"): "a",
    ord("ä"): "ae",
    ord("æ"): "ae",
    ord("ã"): "a",
    ord("å"): "a",
    ord("ā"): "a",
    ord("ç"): "c",
    ord("ć"): "c",
    ord("č"): "c",
    ord("è"): "e",
    ord("é"): "e",
    ord("ê"): "e",
    ord("ë"): "e",
    ord("ē"): "e",
    ord("ė"): "e",
    ord("ę"): "e",
    ord("î"): "i",
    ord("ï"): "i",
    ord("í"): "i",
    ord("ī"): "i",
    ord("į"): "i",
    ord("ì"): "i",
    ord("ł"): "l",
    ord("ñ"): "n",
    ord("ń"): "n",
    ord("ô"): "o",
    ord("ö"): "oe",
    ord("ò"): "o",
    ord("ó"): "o",
    ord("œ"): "oe",
    ord("ø"): "o",
    ord("ō"): "o",
    ord("õ"): "o",
    ord("ß"): "ss",
    ord("ś"): "s",
    ord("š"): "s",
    ord("û"): "u",
    ord("ü"): "ue",
    ord("ù"): "u",
    ord("ú"): "u",
    ord("ū"): "u",
    ord("ÿ"): "y",
    ord("ž"): "z",
    ord("ź"): "z",
    ord("ż"): "z",
    ord("À"): "A",
    ord("Á"): "A",
    ord("Â"): "A",
    ord("Ä"): "Ae",
    ord("Æ"): "Ae",
    ord("Ã"): "A",
    ord("Å"): "A",
    ord("Ā"): "A",
    ord("Ç"): "C",
    ord("Ć"): "C",
    ord("Č"): "C",
    ord("È"): "E",
    ord("É"): "E",
    ord("Ê"): "E",
    ord("Ë"): "E",
    ord("Ē"): "E",
    ord("Ė"): "E",
    ord("Ę"): "E",
    ord("Î"): "I",
    ord("Ï"): "I",
    ord("Í"): "I",
    ord("Ī"): "I",
    ord("Į"): "I",
    ord("Ì"): "I",
    ord("Ł"): "L",
    ord("Ñ"): "N",
    ord("Ń"): "N",
    ord("Ô"): "O",
    ord("Ö"): "Oe",
    ord("Ò"): "O",
    ord("Ó"): "O",
    ord("Œ"): "Oe",
    ord("Ø"): "O",
    ord("Ō"): "O",
    ord("Õ"): "O",
    ord("Ś"): "S",
    ord("Š"): "S",
    ord("Û"): "U",
    ord("Ü"): "Ue",
    ord("Ù"): "U",
    ord("Ú"): "U",
    ord("Ū"): "U",
    ord("Ÿ"): "Y",
    ord("Ž"): "Z",
    ord("Ź"): "Z",
    ord("Ż"): "Z",
}


def key_generator(year: int, authors: List[Dict[str, str]]) -> str:
    """Creates a key for a (new) record."""
    key = str(year)
    for author in authors:
        key += author["last"]
    return key.replace(" ", "").translate(UNICODE_TO_ASCII)
