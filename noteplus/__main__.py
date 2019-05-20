# __main__.py
# Entry point of the noteplus cli application

import click
import sys

from pyfiglet import Figlet
from PyInquirer import prompt

from noteplus.commands.add import add
from noteplus.commands.remove import remove
from noteplus.commands.retrieve import retrieve

from noteplus.setup_db import init_db
from noteplus.interactive_mode import interactive_handler


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.version_option(version='1.0.0', prog_name='noteplus')
@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option('-b', '--banner', 'banner', is_flag=True, help='display the banner')
@click.option('-i', '--interactive', 'interactive', is_flag=True, help='interactive mode')
def main(banner, interactive):
    """Simple note-taking utility"""

    # Create the notes database if non-existent
    init_db()

    if len(sys.argv) == 1:
        raise click.UsageError('Missing option or subcommand')

    if banner:
        b = Figlet(font='slant')
        click.echo(b.renderText('noteplus'))

    if interactive:
        b = Figlet(font='slant')
        click.echo(b.renderText('noteplus'))
        main_selection = interactive_handler()


main.add_command(add)
main.add_command(remove)
main.add_command(retrieve)
