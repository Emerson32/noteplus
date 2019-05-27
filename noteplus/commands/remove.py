# remove.py - Remove a note from the notebook

import click

from noteplus.commands.operations import remove_note, remove_folder
from noteplus.commands.operations import clean_notes, purge_notes


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command('remove', context_settings=CONTEXT_SETTINGS,
               short_help='remove a note')
@click.option('-c', '--clean', 'clean', is_flag=True,
              help='remove all notes (preserves database file)')
@click.option('-p', '--purge', 'purge', is_flag=True,
              help='remove all notes (removes database file)')
@click.option('-f', '--folder', 'folder',
              nargs=1, type=click.Path(writable=True),
              help='remove a folder')
@click.argument('title', required=False, default=None, type=str)
def remove(clean, purge, folder, title):
    """Remove a note from the database"""

    removed_notes = []
    if not (folder or title):

        if clean:
            if click.confirm('\nRemove all notes in the current directory?'):
                removed_notes = clean_notes()

        if purge:
            if click.confirm('\nRemove notes.db?'):
                removed_notes = purge_notes()

    elif folder:
        removed_folder = remove_folder(folder)
        click.echo("Removed: " + removed_folder)

    else:
        removed_notes = remove_note(title=title)

# Print out removed notes
    click.echo()
    for item in removed_notes:
        click.secho("Removed: ", bold=True, fg='cyan', nl=False)
        click.secho(item[0], underline=True)
