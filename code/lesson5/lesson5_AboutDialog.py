from tkinter import *
import Pmw
root = Tk()

Pmw.aboutversion('1.5')
Pmw.aboutcopyright('Copyright Company Name 1999\nAll rights reserved')
Pmw.aboutcontact(
    'For information about this application contact:\n' +
    '  Sales at Company Name\n' +
    '  Phone: (401) 555-1212\n' +
    '  email: info@company_name.com'
    )
about = Pmw.AboutDialog(root, applicationname='About Dialog')

root.mainloop()