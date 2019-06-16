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
            note_menu()
    except KeyError:
        pass


class TitleValidator(Validator):
    def validate(self, document):
        min_length = 4

        if len(document.text) < min_length:
            raise ValidationError(
                message='Title must be at least four characters long',
                cursor_position=len(document.text))


def get_path(home_dir):
    path_input = [
        {
            'type': 'input',
            'name': 'path',
            'message': 'Enter the desired path',
            'default': home_dir,
        }
    ]
    dest = prompt(path_input)
    return dest['path']


def start():
    main_menu = [
            {
                'type': 'list',
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
    choice = prompt(main_menu)
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

    title = prompt(nb_title)
    title = title['nb_title']

    dest = prompt(nb_path)
    dest = dest['path']

    if dest == 'Current Directory':
        dest = os.getcwd()

    else:
        home = str(Path.home())
        dest = get_path(home_dir=home)

    return title, dest


# def note_menu():
#     note_title = [
#         {
#             'type': 'input',
#             'name': 'title',
#             'message': 'Title of the note:',
#             'validate': TitleValidator
#         }
#     ]
#
#     note_path = [
#         {
#             'type': 'list',
#             'name': 'path',
#             'message': 'Where should the note be stored?',
#             'choices': [
#                 Separator('= Specify NoteBook location ='),
#                 'Current Directory',
#                 'Other Location'
#             ]
#         }
#     ]
#
#     notebook_select = [
#     ]
#
#     title_field = prompt(note_title)
#     title_field = title_field['title']

