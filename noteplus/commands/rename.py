# rename.py - Rename a folder, note, or notebook file

import click
import os

from noteplus.commands.basis import NoteBook

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command('rename', context_settings=CONTEXT_SETTINGS,
               short_help='rename a note, notebook, or subject')
@click.option('-n', '--note', 'note',
              nargs=3, type=str, required=False,
              help='Change the title of a note in the current directory'
                   + ' args = [notebook_name, old_title, new_title]')
@click.option('-nb', '--notebook', 'notebook',
              nargs=2, type=str, required=False,
              help='Change the title of a notebook in the current directory')
@click.option('-s', '--subject', 'subject',
              nargs=2, type=str, required=False,
              help='Change the title of a subject in the current directory')
@click.option('-p', '--path', 'path', nargs=1,
              type=click.Path(writable=True),
              default=lambda: os.environ.get('PWD', ''),
              show_default='current directory',
              help='Desired directory to change to before rename')
def rename(note, notebook, subject, path):
    """Change the title of a note, notebook, or subject"""
    if path:
        if os.path.exists(path):
            os.chdir(path)
        else:
            raise click.UsageError("No such directory")

    if subject:
        os.renames(subject[0], subject[1])

        click.echo("Renamed ", nl=False)
        click.secho(subject[0], bold=True, fg='white', nl=False)
        click.echo(" to ", nl=False)
        click.secho(subject[1], bold=True, fg='green')

    elif note:
        if os.path.isfile(note[0]):
            note_book = NoteBook(path=path, file_name=note[0])
            note_book.rename_note(note[1], note[2])

            click.echo("Renamed ", nl=False)
            click.secho(note[1], bold=True, fg='white', nl=False)
            click.echo(" to ", nl=False)
            click.secho(note[2], bold=True, fg='green')
        else:
            raise click.UsageError("No note with that title")

    elif notebook:
        if os.path.isfile(notebook[0]):
            note_book = NoteBook(path=path, file_name=notebook[0])
            note_book.rename(notebook[1])
        else:
            raise click.UsageError("No subject with that title")

    else:
        raise click.UsageError("Missing option")


