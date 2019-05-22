# remove.py - Remove a note from the notebook

import click
import sqlite3

from noteplus.commands.basis import Note

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command('remove', context_settings=CONTEXT_SETTINGS, short_help='remove a note')
@click.option('-p', '--purge', 'purge', is_flag=True, help='remove all notes')
@click.argument('title', required=False, default=None, type=str)
def remove(purge, title):
    """Remove a note from the database"""
    Note.remove(purge=purge, title=title)
