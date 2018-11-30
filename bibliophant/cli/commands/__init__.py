"""This module defines the commands of the application."""

__all__ = ["root_command"]

from .bib import bib as root_command

from . import exporters, get, help, importers, tag_untag
