# remove.py - Remove a note from the notebook

import click
import sqlite3


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command('remove', context_settings=CONTEXT_SETTINGS, short_help='remove a note')
@click.option('-p', '--purge', 'purge', is_flag=True, help='remove all notes')
@click.argument('title', required=False, type=str)
def remove(purge, title):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()

    if purge:
        with conn:
            c.execute('DELETE from notes')

    elif title:
        with conn:
            c.execute('DELETE from notes WHERE title=:title',
                      {'title': title})
