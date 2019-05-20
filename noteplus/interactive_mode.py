from examples import custom_style_2
from PyInquirer import prompt, Separator


def interactive_handler():
    main_selection = prompt(main_menu_selection, style=custom_style_2)
    return main_selection['selection']


main_menu_selection = [
    {
        'type': 'list',
        'name': 'selection',
        'message': 'What do you want to do?',
        'choices': [
            'Create a new folder',
            'Delete a folder ',
            'Retrieve a folder',
            Separator(),
            'Create a new note',
            'Delete a note',
            'Edit a note',
        ]
    }
]
