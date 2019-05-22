# add.py - Create a new entry through the usage of your default editor
#           or through the command line
import click
from os import getcwd

from noteplus.commands.operations import add_note, add_folder

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command('add', context_settings=CONTEXT_SETTINGS, short_help='add note entries')
@click.option('-e', '--editor', 'editor', is_flag=True, help='use buffer to enter note')
@click.option('-f', '--folder', 'folder', nargs=1, type=click.Path(writable=True),
              help='Create a folder with a given name')
@click.option('-n', '--note', 'note', is_flag=True, help='add a new note entry')
@click.argument('title', required=False, default='', type=str)
@click.argument('text', required=False, default='', type=str)
def add(editor, folder, note, title, text):
    """Add a new note to the notebook"""
    cwd = getcwd()

    # Create the new folder and then insert the created note into the folder
    if folder and note:
        folder_path = add_folder(folder)

        added_note = add_note(editor=editor, title=title, text=text, path=folder_path)
        click.echo(added_note.to_string())

    elif folder:
        add_folder(folder)

    elif note:
        added_note = add_note(editor=editor, title=title, text=text, path=cwd)
        click.echo(added_note.to_string())

    else:
        raise click.UsageError('Missing option')
