import click
import npyscreen

from noteplus.selection import Selection

class noteSelectionForm(npyscreen.ActionForm):
    def create(self):
        self.add


    def afterEditing(self):
        self.parentApp.setNextForm(None)


class noteSelectionMenu(nypscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', noteSelectionForm, name='Note Selection Menu')

