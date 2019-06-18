import click
import os
import subprocess
import sys
import time

from examples import custom_style_2
from pathlib import Path
from PyInquirer import prompt, Separator
from PyInquirer import Validator, ValidationError

from noteplus.commands.basis import NoteBook, note_exists

# Global variable to keep track of the current notebook being edited 
curr_nb = None


def interactive_handler():
    try:
        response = start()
        if response == 'Create a notebook':
            nb_title, nb_path = notebook_menu()

            # Initialize a new notebook
            NoteBook(path=nb_path, file_name=nb_title)

        elif response == 'Make a Note':
            while not curr_nb:
                note_path = get_path()
                note_book = select_notebook()

            note_title, note_text = get_note_info()

            subprocess.call(['noteplus', 'add', '-nb', note_book, '-n',
                             note_title, note_text, '-p', note_path])

        elif response == 'Create a new Subject Folder':
            path, title = subject_menu()

            subprocess.call(['noteplus', 'add', '-s', title, '-p', path])

        elif response == 'Delete a Subject Folder':
            path, title = subject_menu()
            subprocess.call('noteplus', 'remove', '-s', title, '-p', path)

    except KeyError:
        pass


# General validator for titles
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


class NoteValidator(Validator):
    def validate(self, document):
        if note_exists(document.text, nb_title=curr_nb.dbfilename):
            raise ValidationError(
                message='Note already exists',
                cursor_position=len(document.text))


def get_path():

    default_path = str(Path.home())

    path_input = [
        {
            'type': 'input',
            'qmark': '[+]',
            'name': 'path',
            'message': 'Enter the desired path: ',
            'default': default_path,
            'validate': PathValidator
        }
    ]

    path_select = [
        {
            'type': 'list',
            'qmark': '[+]',
            'name': 'path',
            'message': 'Specify Location',
            'choices': [
                Separator('= Note Location ='),
                'Current Directory',
                'Other Location'
            ]
        }
    ]

    click.echo()
    dest = prompt(path_select, keyboard_interrupt_msg='Aborted!')
    dest = dest['path']

    if dest == 'Current Directory':
        dest = os.getcwd()
    else:
        dest = prompt(path_input, keyboard_interrupt_msg='Aborted!')
        dest = dest['path']

    os.chdir(path=dest)
    return dest


def get_title(message, validator):
    title_prompt = [
        {
            'type': 'input',
            'qmark': '[+]',
            'name': 'title',
            'message': message,
            'validate': validator
        }
    ]

    title_field = prompt(title_prompt, keyboard_interrupt_msg='Aborted!')
    title_field = title_field['title']

    return title_field


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

    title_field = get_title(message='Notebook title:')

    dest = get_path()

    return title_field, dest


def get_note_info():

    title_field = get_title(message='Note title:', validator=NoteValidator)

    # Edit the note of the text in default editor
    text_field = click.edit()

    if not text_field:
        text_field = 'Empty Note'
    else:
        text_field = text_field.rstrip()

    return title_field, text_field


def select_notebook():
    notebook_select = [
        {
            'type': 'list',
            'qmark': '[+]',
            'name': 'notebook',
            'message': 'Select a notebook',
            'choices': list_notebooks()
        }
    ]

    restart = [
        {
            'type': 'confirm',
            'qmark': '[?]',
            'name': 'restart',
            'message': 'No notebooks found in the give path. Try again?'
        }
    ]

    # Default notebook
    note_book = 'notes.nbdb'

    notebooks = list_notebooks()

    # No notebooks in the specified path
    if len(notebooks) == 0:
        again = prompt(restart, keyboard_interrupt_msg='Aborted!')
        again = again['restart']
        if not again:
            # Path and notebook must be re-chosen
            sys.exit()

    # Ask for notebook
    else:
        note_book = prompt(notebook_select, keyboard_interrupt_msg='Aborted!')
        note_book = note_book['notebook']

        click.echo("\nOpening notebook...\n")
        time.sleep(.5)

        global curr_nb
        curr_nb = NoteBook(path=os.getcwd(), file_name=note_book)

    return note_book


def subject_menu():
    title_field = get_title('Subject title:', validator=TitleValidator)
    dest = get_path()

    return dest, title_field



