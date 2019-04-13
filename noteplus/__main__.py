# __main__.py
# Entry point of the noteplus cli application

import click
from .commands.version import version
from.commands.hello import greeting


@click.group()
def main():
    """Simple note-taking utility"""


main.add_command(version)
main.add_command(greeting)
