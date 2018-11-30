"""This module defines the 'get' command group of the application."""

from ..repl import Command
from .bib import bib


get_group = bib.add_command_group("get", "closed-producing")


@get_group.add("key")
class GetKey(Command):
    def execute(self, arguments, session, config, result=None):
        # TODO
        print("get a record given its key")

    def get_completions(self, document, complete_event):
        # TODO
        return []


@get_group.add("title")
class GetTitle(Command):
    def execute(self, arguments, session, config, result=None):
        # TODO
        print("get a record given (parts of) its title")

    def get_completions(self, document, complete_event):
        # TODO
        return []


@get_group.add("doi")
class GetDoi(Command):
    def execute(self, arguments, session, config, result=None):
        # TODO
        print("get a record given its DOI")

    def get_completions(self, document, complete_event):
        # TODO
        return []


@get_group.add("arxiv")
class GetArXiv(Command):
    def execute(self, arguments, session, config, result=None):
        # TODO
        print("get an article given its arXiv id")

    def get_completions(self, document, complete_event):
        # TODO
        return []


@get_group.add("all")
class GetAll(Command):
    def execute(self, arguments, session, config, result=None):
        # TODO
        print("Passes on all or the <limit> most-recently added records.")

    def get_completions(self, document, complete_event):
        # TODO
        return []


@get_group.add("tag")
class GetTag(Command):
    def execute(self, arguments, session, config, result=None):
        # TODO
        print(
            "Passes on all or the <limit> most-recently added records, which carry the given tag"
        )

    def get_completions(self, document, complete_event):
        # TODO
        return []


@get_group.add("author")
class GetAuthor(Command):
    def execute(self, arguments, session, config, result=None):
        # TODO
        print(
            "Passes on all or the <limit> most-recently added records, which are written by the given author."
        )

    def get_completions(self, document, complete_event):
        # TODO
        return []


@get_group.add("journal")
class GetJournal(Command):
    def execute(self, arguments, session, config, result=None):
        # TODO
        print(
            "Passes on all or the <limit> most-recently added articles, which were published in the given journal."
        )

    def get_completions(self, document, complete_event):
        # TODO
        return []


@get_group.add("publisher")
class GetPublisher(Command):
    def execute(self, arguments, session, config, result=None):
        # TODO
        print(
            "Passes on all or the <limit> most-recently added books, which were published by the given publisher."
        )

    def get_completions(self, document, complete_event):
        # TODO
        return []
