"""This module implements the configuration wizard.
This wizard is called if no configuration is found.
"""

# TODO this is only a first draft


from pathlib import Path
import sys
import json

from .repl import print_error
from .repl.misc import ask_yes_no, ask_for_folder
from prompt_toolkit import prompt


def config_wizard(config_file: Path):
    """The path 'config_file' does not exist.
    This functions creates a config file
    based on some user input.
    It returns the created configuration (JSON / dict).
    """

    config = {}

    ## collections field

    print(
        "\nThe most important information in the configuration file is a list of your bibliophant collections."
    )
    print(
        "If you already have started a collection, please enter the full or relative path of its root folder."
    )
    print(
        "If you want to start a new collection, create an empty folder and provide the path."
    )
    print(
        "You may use '~' to refer to your home directory (example: '~/my_collection')."
    )
    print(
        "\The first collection you specify will be opened by default whenever you run 'bib' without the '-c' option."
    )

    collections = [
        str(ask_for_folder("Enter the root path of your default collection: "))
    ]

    while ask_yes_no("Do you want to add another collection?"):
        collections.append(
            str(ask_for_folder("Enter the root path of your collection: "))
        )

    config["collections"] = collections

    ## open_pdf field

    print(
        "\nThe next thing is to tell bibliophant about the shell command it should use to launch the PDF viewer."
    )
    print(
        "On macOS you can for example just specify 'open' to use your default application."
    )

    config["open_pdf"] = prompt("Enter the command used to open PDF documents: ")

    ## open_folder field

    print("\nNow specify the command to open a record folder.")
    print("On macOS it makes even more sense here to use 'open'.")

    config["open_folder"] = prompt("Enter the command used to open record folders: ")

    ## delete_folder

    print("\nPlease also specify a command used to delete a record folder.")
    print("A popular option is 'rm -Rf'.")
    print("A safer option is 'rmtrash'.")
    print("On macOS, you can install this command with 'brew install rmtrash'.")
    print("If you want to use git to take care of your collections, use 'git rm'.")

    config["delete_folder"] = prompt(
        "Enter the command used to delete record folders: "
    )

    ## complete

    try:
        with open(config_file, "w+") as file:  # mode 'w+' creates file
            json.dump(config, file, indent=4)
    except:
        print_error(
            f"There was a problem with storing the configuration to {config_file}."
        )
        raise

    print("\nThe following configuration file was created:")
    print(json.dumps(config, indent=4))
    print("If you are not happy with it please edit it.")
    print("Of course you can also delete it, and let the wizard help you again.")

    print("\nThat's it!\n")

    return config
