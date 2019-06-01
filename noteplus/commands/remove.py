# remove.py - Remove a note from the notebook

import click
import os

from noteplus.commands.operations import remove_note, remove_folder
from noteplus.commands.operations import clean_notes, purge_notes

from noteplus.commands.basis import NoteBook
from noteplus.commands.basis import Subject


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command('remove', context_settings=CONTEXT_SETTINGS,
               short_help='remove a note')
@click.option('-c', '--clean', 'clean', is_flag=True,
              help='remove all notes (preserves database file)')
@click.option('-p', '--purge', 'purge', is_flag=True,
              help='remove all notes (removes database file)')
@click.option('-s', '--subject', 'subject',
              nargs=1, type=click.Path(writable=True),
              help='remove a folder')
@click.argument('nb_title', required=True, default='notes.db', type=str)
def remove(clean, purge, subject, nb_title):
    """Remove a note from the database"""

    removed_notes = []

    if subject:
        # TODO: Correct the name of the removed directory
        subject_name = os.path.basename(subject.rstrip('/'))
        subj = Subject(path=subject, name=subject_name)
        removed_subject = subj.remove()
        click.echo("Removed: " + removed_subject)

    else:
        note_book = NoteBook(os.getcwd(), nb_title)

        if clean:
            if click.confirm('\nRemove all notes in the current directory?'):
                removed_notes = note_book.clean_notes()

        if purge:
            if click.confirm('\nRemove notes file?'):
                removed_notes = note_book.purge_notes()

# Print out removed notes
    click.echo()
    for item in removed_notes:
        click.secho("Removed: ", bold=True, nl=False)
        click.secho(item[0], fg='red', underline=True)
    
    click.echo()
