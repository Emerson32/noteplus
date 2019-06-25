#!/usr/bin/env python
# __main__.py
# Entry point of the noteplus cli application

import click
import sys

from pyfiglet import Figlet

from noteplus.commands.add import add
from noteplus.commands.edit import edit
from noteplus.commands.remove import remove
from noteplus.commands.rename import rename
from noteplus.commands.retrieve import retrieve
from noteplus.commands.interactive import interactive_handler

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.version_option(version='1.0.0', prog_name='noteplus')
@click.group(invoke_without_command=True,
             context_settings=CONTEXT_SETTINGS)
@click.option('-b', '--banner', 'banner', is_flag=True,
              type=bool, help='display the banner')
@click.option('-i', '--interactive', 'interactive',
              is_flag=True, type=bool,
              help='interactive mode')
def main(banner, interactive):
    """Simple note-taking utility"""

    if len(sys.argv) == 1:
        raise click.UsageError('Missing option or subcommand')

    if banner:
        b = Figlet(font='slant')
        click.echo(b.renderText('noteplus'))

    if interactive:
        interactive_handler()


main.add_command(add)
main.add_command(edit)
main.add_command(remove)
main.add_command(rename)
main.add_command(retrieve)
