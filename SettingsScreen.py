# Kivy modules
from kivy.uix.floatlayout import FloatLayout

# Tkinter modules
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import tkinter.scrolledtext

# Other & self-defined modules
import Controller as c

# Global function to center window for all screens
def centerWindow(window,r1,r2,d1,d2):
    window.resizable(False,False)
    windowWidth = window.winfo_reqwidth()
    windowHeight = window.winfo_reqheight()
    positionRight = int(window.winfo_screenwidth() / r1 - windowWidth / r2)
    positionDown = int(window.winfo_screenheight() / d1 - windowHeight / d2)
    window.geometry('+{}+{}'.format(positionRight, positionDown))

# Global function to customize error-popup window
def show_error_popup(title,msg):
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showerror(title,msg)
    root.destroy()



class Settings_Screen(FloatLayout):
    def back_press(self):
        pass

    def create_press(self):
        pass

    def manage_press(self):
        self.showManageWindow()

    def showManageWindow(self):
        managePop = tk.Tk()
        managePop.geometry('540x465')
        managePop.title('Manage Existing Models')
        centerWindow(managePop, 2.6, 2, 2.9, 2)

        top_frame = Frame(managePop)
        mid_frame = Frame(managePop)
        btm_frame = Frame(managePop)
        cmb_values = c.getModelDetails(names=True)
        cmb = ttk.Combobox(top_frame, width=15, values=cmb_values, justify=tk.CENTER)
        label = Label(mid_frame, text='Model Details')
        textArea = tk.scrolledtext.ScrolledText(mid_frame, height=20, width=55)
        btn1 = ttk.Button(btm_frame, text='Edit Details', pad=3, command=lambda: self.edit_press(widgets=[textArea, btn2, btn3, cmb, btn1]))

        btn2 = ttk.Button(btm_frame, text='Use Model', pad=3, command=lambda: self.change_press(widgets=[textArea, btn2, btn3, cmb], \
                                                                                                current_model=cmb['values'][0], \
                                                                                                model_name=cmb.get()))

        btn3 = ttk.Button(btm_frame, text='Delete Model', pad=3, command=lambda: self.delete_press(widgets=[textArea, btn2, btn3, cmb], \
                                                                                                   model_name=cmb.get()))

        cmb.set(cmb_values[0])
        cmb.bind('<<ComboboxSelected>>', lambda event: self.updateManageWindow(widgets=[textArea, btn2, btn3, cmb], model_name=cmb.get()))
        cmb.pack()
        top_frame.pack(pady=15)

        label.pack(pady=5)
        textArea.pack(fill=tk.BOTH)
        mid_frame.pack(padx=15)
        btn1.grid(row=0, column=1, padx=25)
        btn2.grid(row=0, column=2, padx=25)
        btn3.grid(row=0, column=3, padx=25)
        btm_frame.pack(pady=15)
        self.updateManageWindow([textArea, btn2, btn3, cmb], cmb.get())
        managePop.mainloop()

    def updateManageWindow(self, widgets, model_name):
        lines, disableBtn = c.getModelDetails(details=True, model_name=model_name)
        model_details = ''
        for i in range(len(lines)):
            model_details += lines[i]

        # Update combobox values
        widgets[3]['values'] = c.getModelDetails(names=True)
        widgets[3].set(model_name)

        # Disable 2 buttons if model_in_use is selected
        widgets[1]['state'] = 'disabled' if disableBtn == True else 'normal'
        widgets[2]['state'] = 'disabled' if disableBtn == True else 'normal'

        # Erase previous & insert new
        widgets[0].config(state=NORMAL)
        widgets[0].delete(1.0, END)
        widgets[0].insert(INSERT, model_details)
        widgets[0].config(state=DISABLED)

    def edit_press(self, widgets):
        editPop = tk.Tk()
        editPop.title('Edit Details')
        editPop.protocol('WM_DELETE_WINDOW', lambda: self.callback(editPop, widgets))
        centerWindow(editPop, 2.35, 2, 2.325, 2)

        frame = Frame(editPop)
        label1 = Label(frame, text='Model Name: ')
        label2 = Label(frame, text='Dataset: ')
        label3 = Label(frame, text='Description: ')
        entry1 = ttk.Entry(frame)
        entry2 = ttk.Entry(frame)
        entry3 = tk.scrolledtext.ScrolledText(frame, height=10, width=35)
        btn = ttk.Button(editPop, text='OK', command=lambda: self.updateDetails(window=editPop, widgets=widgets, \
                                                                                input_list=[entry1.get(), entry2.get(), entry3.get(1.0, END)], \
                                                                                detail_list=[name, dataset, description],
                                                                                entries=[entry1,entry2,entry3]))
        label1.grid(sticky='W', row=0, column=0, pady=5)
        entry1.grid(sticky='W', row=0, column=1, pady=5)
        label2.grid(sticky='W', row=1, column=0, pady=5)
        entry2.grid(sticky='W', row=1, column=1, pady=5)
        label3.grid(sticky='NW', row=2, column=0, pady=5)
        entry3.grid(sticky='W', row=2, column=1, pady=5)
        frame.pack(padx=15, pady=5)
        btn.pack(padx=15, pady=10)

        widgets[1].configure(state='disable')
        widgets[2].configure(state='disable')
        widgets[3].configure(state='disable')
        widgets[4].configure(state='disable')
        model_details, _ = c.getModelDetails(details=True, edit=True, model_name=widgets[3].get())
        name = (model_details[0].split(': ')[1])[:-1]
        dataset = (model_details[4].split(': ')[1])[:-1]
        description = (model_details[-1])
        entry1.insert(INSERT, name)
        entry2.insert(INSERT, dataset)
        entry3.insert(INSERT, description)
        editPop.mainloop()

    def callback(self, window, widgets):
        # Close window & enable widgets
        window.destroy()
        widgets[1].configure(state='normal')
        widgets[2].configure(state='normal')
        widgets[3].configure(state='normal')
        widgets[4].configure(state='normal')
        self.updateManageWindow(widgets=widgets, model_name=widgets[3].get())

    def updateDetails(self, window, widgets, input_list, detail_list, entries):
        input_list = c.processInputDetails(input_list)
        name = input_list[0]
        dataset = input_list[1]
        description = input_list[2]

        if name == '' or dataset == '' or description == '':
            show_error_popup('Error','Please make sure no fields are empty.')
            entries[0].delete(0, 'end')
            entries[1].delete(0, 'end')
            entries[2].delete('1.0', 'end')
            entries[0].insert(0, detail_list[0])
            entries[1].insert(0, detail_list[1])
            entries[2].insert(INSERT, detail_list[2])
            window.lift()
        else:
            changed = c.updateDetails(input_list, detail_list)

            # If changed name is duplicate
            if changed == -1:
                tk.messagebox.showerror('Name Error','The same model name already exists. Please try other names.')
                entries[0].delete(0,'end')
                entries[0].insert(0,detail_list[0])
                window.lift()

            elif changed is True:
                window.destroy()
                tk.messagebox.showinfo('Details changed', 'Edit model details successful.')
                # Destroy editPop & update managePop
                widgets[3]['values'] = c.getModelDetails(names=True)
                widgets[1].configure(state='normal')
                widgets[2].configure(state='normal')
                widgets[3].configure(state='normal')
                widgets[4].configure(state='normal')
                self.updateManageWindow(widgets=widgets, model_name=input_list[0])

            elif changed is False:
                window.destroy()
                widgets[1].configure(state='normal')
                widgets[2].configure(state='normal')
                widgets[3].configure(state='normal')
                widgets[4].configure(state='normal')
                self.updateManageWindow(widgets=widgets, model_name=detail_list[0])


    def change_press(self, widgets, current_model, model_name):
        root = tk.Tk()
        root.withdraw()
        ans = tk.messagebox.askquestion('Change Model', 'Do you wish to change the working model from \'{}\' to \'{}\'?'. \
                                        format(current_model, model_name))
        if ans == 'yes':
            c.changeModel(model_name)
            tk.messagebox.showinfo('Model Changed', 'The current working model has been changed to \'{}\'.'.format(model_name))
            self.updateManageWindow(widgets, model_name)
        root.destroy()

    def delete_press(self, widgets, model_name):
        root = tk.Tk()
        root.withdraw()
        ans = tk.messagebox.askquestion('Delete Model', 'Do you wish to delete model \'{}\'?'.format(model_name))
        if ans == 'yes':
            c.deleteModel(model_name)
            tk.messagebox.showinfo('Model Deleted', 'Model \'{}\' has been deleted.'.format(model_name))
            self.updateManageWindow(widgets, widgets[3]['values'][0])
        root.destroy()
