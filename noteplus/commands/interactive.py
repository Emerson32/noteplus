import click
import subprocess
import os

from examples import custom_style_2
from pathlib import Path
from PyInquirer import prompt, Separator
from PyInquirer import Validator, ValidationError

from noteplus.commands.basis import NoteBook


def interactive_handler():
    try:
        response = start()
        if response == 'Create a notebook':
            nb_title, nb_path = notebook_menu()

            # Initialize a new notebook
            note_book = NoteBook(path=nb_path, file_name=nb_title)

        elif response == 'Make a Note':
            note_book, note_title, note_text, note_path = note_menu()

            subprocess.call(['noteplus', 'add', '-nb', note_book, '-n',
                             note_title, note_text, '-p', note_path])
    except KeyError:
        pass


class TitleValidator(Validator):
    def validate(self, document):
        min_length = 4

        if len(document.text) < min_length:
            raise ValidationError(
                message='Title must be at least four characters long',
                cursor_position=len(document.text))


class PathValidator(Validator):
    def validate(self, document):

        if not os.path.exists(document.text):
            raise ValidationError(
                message='Path does not exist',
                cursor_position=len(document.text))


def get_path():

    default_path = str(Path.home())

    path_input = [
        {
            'type': 'input',
            'name': 'path',
            'message': 'Enter the desired path',
            'default': default_path,
            'validate': PathValidator
        }
    ]

    dest = prompt(path_input, keyboard_interrupt_msg='Aborted!')
    dest = dest['path']
    return dest


def list_notebooks():
    notebook_list = []

    for file in os.listdir(os.getcwd()):
        if file.endswith('.nbdb'):
            notebook_list.append(file.rstrip('.nbdb'))

    return notebook_list


def start():
    main_menu = [
            {
                'type': 'list',
                'qmark': '[+]',
                'name': 'selection',
                'message': 'What do you want to do?',
                'choices': [
                    'Create a notebook',
                    'Make a Note',
                    'Create a new Subject Folder',
                    'Delete a notebook',
                    'Delete a note',
                    'Delete a Subject Folder'
                ]
            }
    ]
    choice = prompt(main_menu, keyboard_interrupt_msg='Aborted!')
    return choice['selection']


def notebook_menu():
    nb_title = [
        {
            'type': 'input',
            'name': 'nb_title',
            'message': 'Notebook Title:',
            'default': 'notebook',
            'validate': TitleValidator
        }
    ]
    nb_path = [
            {
                'type': 'list',
                'name': 'path',
                'message': 'Where should the notebook be stored?',
                'choices': [
                    Separator('= Notebook Location ='),
                    'Current Directory',
                    'Other Location'
                ]
            }
    ]

    title = prompt(nb_title, keyboard_interrupt_msg='Aborted!')
    title = title['nb_title']

    dest = prompt(nb_path, keyboard_interrupt_msg='Aborted!')
    dest = dest['path']

    if dest == 'Current Directory':
        dest = os.getcwd()

    else:
        dest = get_path()

    return title, dest


def note_menu():

    note_title = [
        {
            'type': 'input',
            'name': 'title',
            'message': 'Title of the note:',
            'validate': TitleValidator
        }
    ]

    note_path = [
        {
            'type': 'list',
            'name': 'path',
            'message': 'Where should the note be stored?',
            'choices': [
                Separator('= Note Location ='),
                'Current Directory',
                'Other Location'
            ]
        }
    ]

    restart = [
        {
            'type': 'confirm',
            'name': 'restart',
            'message': 'No notebooks found in the give path. Try again?'
        }
    ]

    notebook_select = [
        {
            'type': 'list',
            'name': 'notebook',
            'message': 'Which notebook would you like to use?',
            'choices': list_notebooks()
        }
    ]

    # Set default notebook to notes.nbdb
    note_book = 'notes.nbdb'

    # May need to loop process
    while True:
        click.echo()
        dest = prompt(note_path, keyboard_interrupt_msg='Aborted!')
        dest = dest['path']

        if dest == 'Current Directory':
            dest = os.getcwd()
        else:
            dest = get_path()

        os.chdir(path=dest)

        notebooks = list_notebooks()

        # No notebooks in the specified path
        if len(notebooks) == 0:
            again = prompt(restart, keyboard_interrupt_msg='Aborted!')
            again = again['restart']
            if again:
                continue

        # Ask for notebook
        else:
            note_book = prompt(notebook_select, keyboard_interrupt_msg='Aborted!')
            note_book = note_book['notebook']
            break

    title_field = prompt(note_title, keyboard_interrupt_msg='Aborted!')
    title_field = title_field['title']

    # Edit the note of the text in default editor
    text_field = click.edit()

    if not text_field:
        text_field = 'Empty Note'

    return note_book, title_field, text_field, dest



