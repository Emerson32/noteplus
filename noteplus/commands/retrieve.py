# retrieve.py - Returns a list of note entries within the database

import click
import sqlite3


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command('retrieve', context_settings=CONTEXT_SETTINGS, short_help='retrieve note entries')
@click.option('-a', '--all', 'all_notes', is_flag=True, help='retrieve all note entries')
@click.option('-t', '--title', 'note_title', nargs=1, type=str, help='retrieve a note based on its title')
@click.option('-n', '--note', 'note', nargs=1, type=str, help='retrieve a note based on the note')
def retrieve(all_notes, note_title, note):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()

    if all_notes:
        with conn:
            c.execute('SELECT * FROM notes')

        results = c.fetchall()
        for item in results:
            print()
            print('Title: ' + item[0])
            print('Note: ' + item[1])
            print('Time: ' + item[2])

    elif note_title:
        with conn:
            c.execute("SELECT * FROM notes WHERE title=:title", {'title': note_title})

        results = c.fetchall()
        for item in results:
            click.echo()
            click.echo('Title: ' + item[0])
            click.echo('Note: ' + item[1])
            click.echo('Time: ' + item[2])

    elif note:
        with conn:
            c.execute("Select * FROM notes WHERE note=:note", {'note': note})

        results = c.fetchall()
        for item in results:
            print()
            print('Title: ' + item[0])
            print('Note: ' + item[1])
            print('Time: ' + item[2])

    else:
        raise click.UsageError('Missing option')

