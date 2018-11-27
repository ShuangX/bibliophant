# bibliophant (WIP)

A tool for managing bibliographies and PDF documents.

<img src="https://github.com/MarkusLohmayer/bibliophant/blob/master/bibliophant.png?raw=true" width="150" />


## Introduction

Bibliophant (`bib`) can manage multiple collections simultaneously.

Each **collection** is a folder on your drive which contains:
- a SQLite database file (`bibliophant.db`)
- one subfolder for each bibliographic record

The name of each **record folder** is `<key>` and it contains:
- a JSON file (`<key>.json`)
- often a PDF file (`<title>.pdf`)

A `<key>` is a unique identifier of a record.
- It might look like `<YYYY><Last><Last>`.
- It begins with the year of publication of the record and
continues with (a list of) the last name(s) of the author(s).
- It may not contain whitespace or non-ASCII characters.
- It is also used as the `BibTeX` key of the record.

Of course you can put any files that you associate with a record into its folder.

You might consider using `git` to keep track of the changes to your record folder.

Bibliophant offers you a command-line interface which is built with [Python Prompt Toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit).

You can also leverage its functionality from Python.
Bibliophant talks to [SQLite](https://www.sqlite.org) through
[SQLAlchemy](https://www.sqlalchemy.org).


## Getting started

TODO

1. installing bibliophant with pip
2. initializing a collection
3. setting a shell variable pointing to your default collection

## News

TODO

## Documentation

If you have installed bibliophant, you can access further documentation by typing
```
$ bib help
```
