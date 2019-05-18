# __main__.py
# Entry point of the noteplus cli application

import click

from noteplus.commands.add import add
from noteplus.commands.remove import remove
from noteplus.commands.retrieve import retrieve
import noteplus.commands.test as test

from noteplus.setup_db import init_db


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.version_option(version='1.0.0', prog_name='noteplus')
@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    """Simple note-taking utility"""

    # Create the notes database if non-existent
    init_db()


main.add_command(add)
main.add_command(remove)
main.add_command(retrieve)
main.add_command(test)
