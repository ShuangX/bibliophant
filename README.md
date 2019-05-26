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

Development installation:

It is assumed that Python 3 is installed.

1. (fork and) clone the repository
```
cd ...
git clone https://github.com/MarkusLohmayer/bibliophant
cd bibliophant
```
Of course, you can also fork the repository on GitHub which allows you to contribute to the project by suggesting pull requests.
```
git clone https://github.com/<your user>/bibliophant
cd bibliophant
git remote add upstream https://github.com/MarkusLohmayer/bibliophant
```

2. create a virtual environment
```
cd .../bibliophant
python3 -m venv venv
source venv/bin/activate
pip install .
```
you can create a symlink to the bib command from some directory that is in your $PATH:
```
ln -s .../bibliophant/venv/bin/bib .../bib
```


## News

TODO

## Documentation

If you have installed bibliophant, you can access further documentation by typing
```
$ bib help
```
