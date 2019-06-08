import npyscreen
from noteplus.selection import Selection


class mainMenuForm(npyscreen.ActionForm):
    def create(self):
        op_list = ['Create a New Folder', 'Retrieve a Folder', 'Delete a Folder',
                   'Create a New Note', 'Edit a Note', 'Delete a Note']

        self.selection = self.add(npyscreen.TitleMultiLine, name='Choose One:', values=op_list)

    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def on_ok(self):
        # selection = Selection(self.selection.value)

        if self.selection.value == 5:
            purge_notes()

        self.editing = False

    def on_cancel(self):
        self.editing = False


class NotePlusApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', mainMenuForm, name='Noteplus')
