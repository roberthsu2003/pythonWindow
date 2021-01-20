from tkinter import *
import Pmw
import string


class Shell:
    def __init__(self, title=''):
        self.root = Tk()
        self.root.option_add('*font', ('verdana', 12, 'bold'))
        Pmw.initialise(self.root)
        self.root.title(title)

    def doBaseForm(self, master):
        # Create the Balloon.
        self.balloon = Pmw.Balloon(master)

        self.menuBar = Pmw.MenuBar(master, hull_borderwidth=1,
                                   hull_relief='raised',
                                   hotkeys=1, balloon=self.balloon)
        self.menuBar.pack(fill='x')
        self.menuBar.addmenu('File', 'Exit')
        self.menuBar.addmenuitem('File', 'command',
                                 'Exit the application',
                                 label='Exit', command=self.exit)
        self.menuBar.addmenu('View', 'View user information')
        self.menuBar.addmenuitem('View', 'command',
                                 'Get user information',
                                 label='Get info',
                                 command=self.getStatus)
        self.menuBar.addmenu('Help', 'About Example 10-4', side='right')
        self.menuBar.addmenuitem('Help', 'command',
                                 'Get information on application',
                                 label='About...', command=self.help)

        self.dataFrame = Frame(master)
        self.dataFrame.pack(fill='both', expand=1)

        self.infoFrame = Frame(self.root,
                               bd=1, relief='groove')
        self.infoFrame.pack(fill='both', expand=1, padx=10)

        self.statusBar = Pmw.MessageBar(master, entry_width=40,
                                        entry_relief='groove',
                                        labelpos='w',
                                        label_text='')
        self.statusBar.pack(fill='x', padx=10, pady=10)

        # Add balloon text to statusBar
        self.balloon.configure(statuscommand=self.statusBar.helpmessage)

        # Create about dialog.
        Pmw.aboutversion('10.4')
        Pmw.aboutcopyright('Copyright My Company 1999\nAll rights reserved')
        Pmw.aboutcontact(
            'For information about this application contact:\n' +
            '  My Help Desk\n' +
            '  Phone: 800 555-1212\n' +
            '  email: help@my.company.com'
        )
        self.about = Pmw.AboutDialog(master,
                                     applicationname='Example 10-4')
        self.about.withdraw()

    def exit(self):
        import sys
        sys.exit(0)

    def getStatus(self):
        username = self.userName.get()
        cardnumber = self.cardNumber.get()
        self.img = PhotoImage(file='%s.gif' % username)
        self.pictureID['image'] = self.img
        self.userInfo.importfile('%s.txt' % username)
        self.userInfo.configure(label_text=username)

    def help(self):
        self.about.show()

    def doDataForm(self):
        self.userName = Pmw.EntryField(self.dataFrame, entry_width=8,
                                       value='',
                                       modifiedcommand=self.upd_username,
                                       label_text='User name:      ',
                                       labelpos=W, labelmargin=1)
        self.userName.place(relx=.20, rely=.325, anchor=W)

        self.cardNumber = Pmw.EntryField(self.dataFrame, entry_width=8,
                                         value='',
                                         modifiedcommand=self.upd_cardnumber,
                                         label_text='Card number:  ',
                                         labelpos=W, labelmargin=1)
        self.cardNumber.place(relx=.20, rely=.70, anchor=W)

    def doInfoForm(self):
        self.pictureID = Label(self.infoFrame, bd=0)
        self.pictureID.pack(side='left', expand=1)

        self.userInfo = Pmw.ScrolledText(self.infoFrame,
                                         borderframe=1,
                                         labelpos='n',
                                         usehullsize=1,
                                         hull_width=270,
                                         hull_height=100,
                                         text_padx=10,
                                         text_pady=10,
                                         text_wrap='none')

        self.userInfo.configure(text_font=('verdana', 8))
        self.userInfo.pack(fill='both', expand=1)

    def upd_username(self):
        upname = string.upper(self.userName.get())
        if upname:
            self.userName.setentry(upname)

    def upd_cardnumber(self):
        valid = self.cardNumber.get()
        if valid:
            self.cardNumber.setentry(valid)


if __name__ == '__main__':
    shell = Shell(title='Example 10-4')
    shell.root.geometry("%dx%d" % (400, 350))
    shell.doBaseForm(shell.root)
    shell.doDataForm()
    shell.doInfoForm()
    shell.root.mainloop()



