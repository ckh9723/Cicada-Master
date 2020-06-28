# Kivy modules
from kivy.uix.floatlayout import FloatLayout

# Tkinter modules
import tkinter as tk
from tkinter import *
from tkinter import ttk

# Self-defined modules
import Controller as c



# Global functions
def centerWindow(window,r1,r2,d1,d2):
    window.resizable(False,False)
    windowWidth = window.winfo_reqwidth()
    windowHeight = window.winfo_reqheight()
    positionRight = int(window.winfo_screenwidth() / r1 - windowWidth / r2)
    positionDown = int(window.winfo_screenheight() / d1 - windowHeight / d2)
    window.geometry('+{}+{}'.format(positionRight, positionDown))

def show_tutorial():
    tutoPop = tk.Tk()
    tutoPop.title('Tutorial')
    centerWindow(tutoPop,2.4,2,2,2)
    tutoPop.protocol('WM_DELETE_WINDOW', lambda: close_tutorial(tutoPop,checked.get()))

    grid_frame = Frame(tutoPop)
    label_t = Label(tutoPop, text='-------------------- WELCOME TO CICADA MASTER --------------------')
    icon = ttk.Label(grid_frame, image="::tk::icons::question")
    label = ttk.Label(grid_frame, text='An already-built classification model is used by default. You can create\n ' \
                                       + 'a new model or view details of the default model through the \'Model\n ' \
                                       + 'Settings\' page.')
    checked = tk.IntVar()
    cbtn = Checkbutton(tutoPop, text='Do not show again', variable=checked)
    btn = ttk.Button(tutoPop, text='OK', command=lambda: close_tutorial(tutoPop,checked.get()))

    label_t.pack(padx=20,pady=10)
    icon.grid(row=0, column=0, padx=10)
    label.grid(row=0, column=1, padx=10)
    grid_frame.pack(padx=10)
    cbtn.pack(pady=5)
    btn.pack(pady=10)
    tutoPop.mainloop()

def close_tutorial(window,checked):
    if checked == 1:
        c.setConfigNoHelp('Tutorial')
    window.destroy()



class Main_Screen(FloatLayout):
    def classify_press(self):
        pass

    def settings_press(self):
        pass
