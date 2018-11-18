"""This package defines all subcommands for the interactive user interface."""

from .article import article_subcommands
from .author import author_subcommands
from .book import book_subcommands
from .record import record_subcommands
from .tag import tag_subcommands


# register all available subcommand groups
command_groups = {
    "article": article_subcommands,
    "author": author_subcommands,
    "book": book_subcommands,
    "record": record_subcommands,
    "tag": tag_subcommands,
}
