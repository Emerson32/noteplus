# edit.py - Edit the contents of a note entry
import click
import sqlite3
import os

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command('edit', context_settings=CONTEXT_SETTINGS,
               short_help='edit a note')
@click.option('-r', '--rename-choice', 'rename_choice',
              type=click.Choice(['note', 'folder']),
              help='rename a note or folder (default=note)')
@click.argument('old_title', required=False, type=str)
@click.argument('new_title', required=False, type=str)
def edit(rename_choice, old_title, new_title):
    """Make changes to a note or folder"""
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()

    if rename_choice:
        if not (old_title or new_title):
            raise click.UsageError('Missing title argument')

    if rename_choice == 'folder':
        os.rename(old_title, new_title)

    else:
        with conn:
            c.execute('SELECT * FROM notes WHERE title=:title',
                      {'title': old_title})

        results = c.fetchall()

        if len(results) == 0:
            raise click.UsageError('No such note with that title')
        elif len(results) > 1:
            # Present user with menu to choose a note
            pass
        else:
            # Update one entry with the new title
            with conn:
                c.execute('''UPDATE notes set title= ?
                          WHERE title= ? ''',
                          (new_title, old_title))
