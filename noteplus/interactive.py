import npyscreen


class mainMenuForm(npyscreen.ActionForm):
    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def on_ok(self):
        self.editing = False
        self.set_value(self.selection)

    def on_cancel(self):
        self.editing = False

    def create(self):
        op_list = ['Create a New Folder', 'Retrieve a Folder', 'Delete a Folder',
                'Create a New Note', 'Edit a Note', 'Delete a Note']

        self.selection = self.add(npyscreen.TitleMultiLine, name='Choose One:', values=op_list)


class NotePlusApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', mainMenuForm, name='Noteplus')
