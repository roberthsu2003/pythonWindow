from tkinter import *
from tkinter.simpledialog import Dialog
from tkinter import messagebox


class GetPassword(Dialog):

    def body(self, master):
        self.title("Enter New Password")

        Label(master, text='Old Password:').grid(row=0, sticky=W)
        Label(master, text='New Password:').grid(row=1, sticky=W)
        Label(master, text='Enter New Password Again:').grid(row=2, sticky=W)

        self.oldpw = Entry(master, width=16, show='*')
        self.newpw1 = Entry(master, width=16, show='*')
        self.newpw2 = Entry(master, width=16, show='*')

        self.oldpw.grid(row=0, column=1, sticky=W)
        self.newpw1.grid(row=1, column=1, sticky=W)
        self.newpw2.grid(row=2, column=1, sticky=W)
        return self.oldpw

    def apply(self):
        opw = self.oldpw.get()
        npw1 = self.newpw1.get()
        npw2 = self.newpw2.get()

        if not npw1 == npw2:
            messagebox.showerror('Bad Password',
                                   'New Passwords do not match')
        else:
            # This is where we would set the new password...
            pass


root = Tk()
dialog = GetPassword(root)