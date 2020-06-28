# Kivy modules
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout

# Tkinter modules
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import tkinter.scrolledtext
from tkinter import filedialog

# Others
import multiprocessing
import Controller as c


# Global functions
def centerWindow(window,r1,r2,d1,d2):
    window.resizable(False,False)
    windowWidth = window.winfo_reqwidth()
    windowHeight = window.winfo_reqheight()
    positionRight = int(window.winfo_screenwidth() / r1 - windowWidth / r2)
    positionDown = int(window.winfo_screenheight() / d1 - windowHeight / d2)
    window.geometry('+{}+{}'.format(positionRight, positionDown))

def show_error_popup(title,msg):
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showerror(title,msg)
    root.destroy()

def show_help(tutorial=False):
    help_pop = tk.Tk()
    help_pop.title('Classify Help')
    centerWindow(help_pop, 2.5, 2, 2.1, 2)
    help_pop.protocol('WM_DELETE_WINDOW', lambda: close_help(help_pop))

    grid_frame = Frame(help_pop)
    right_frame = Frame(grid_frame)
    icon = Label(grid_frame, image="::tk::icons::question")
    label1 = ttk.Label(right_frame, text='Cicada Master provides two ways to perform species classification:')
    label2 = ttk.Label(right_frame, text='1) Input Features - Classify a single data with feature values input by' \
                                         + '\n                                 the user. Quick & easy.')
    label3 = ttk.Label(right_frame,
                       text='2) Upload File - Classify multiple data in an Excel file(.xlsx). Results will' \
                            + ' \n                            also be stored as an Excel file. See \'HELP\' for more' \
                            + ' \n                            info on how to upload a proper Excel file.')
    btn = ttk.Button(help_pop, text="OK", command=help_pop.destroy)
    icon.grid(row=0, column=0, sticky='ne', padx=5, pady=7)
    label1.pack(fill='x', pady=15)
    label2.pack(fill='x', pady=5)
    label3.pack(fill='x', pady=7)
    right_frame.grid(row=0, column=1, padx=5)
    grid_frame.pack(padx=20, pady=7)

    if tutorial is True:
        checked = IntVar()
        cbtn = Checkbutton(help_pop, text='Do not show again', variable=checked)
        cbtn.pack(padx=20,pady=3)
        btn['command'] = lambda: close_help(help_pop,checked=checked.get())
        help_pop.protocol('WM_DELETE_WINDOW', lambda: close_help(help_pop, checked=checked.get()))

    btn.pack(padx=20, pady=10)
    help_pop.update()
    help_pop.geometry('{}x{}'.format(help_pop.winfo_width()+5, help_pop.winfo_height()+5))
    help_pop.mainloop()

def close_help(window,checked=None):
    if checked == 1:
        c.setConfigNoHelp('Classify')
    window.destroy()



class Classify_Screen(FloatLayout):
    input_dict = {}
    value_txt = ObjectProperty(None)
    file_path = ObjectProperty(None)
    default_value_txt = '[No values]'
    default_file_path = '[No file chosen]'
    full_file_path = ''

    # Help-popup methods
    def show_help(self,tutorial=False):
        help_pop = tk.Tk()
        help_pop.title('Classify Help')
        centerWindow(help_pop, 2.45, 2, 2.1, 2)
        help_pop.protocol('WM_DELETE_WINDOW', lambda: self.close_help(help_pop))

        grid_frame = Frame(help_pop)
        right_frame = Frame(grid_frame)
        icon = Label(grid_frame, image="::tk::icons::question")
        label1 = ttk.Label(right_frame, text='Cicada Master provides two ways to perform species classification:')
        label2 = ttk.Label(right_frame, text='1) Input Features - Classify a single data with feature values input by' \
                                             + '\n                                 the user. Quick & easy.')
        label3 = ttk.Label(right_frame,
                           text='2) Upload File - Classify multiple data in an Excel file(.xlsx). Results will' \
                                + ' \n                            also be stored as an Excel file. See \'HELP\' for more' \
                                + ' \n                            info on how to upload a proper Excel file.')
        btn = ttk.Button(help_pop, text="OK", command=help_pop.destroy)
        icon.grid(row=0, column=0, sticky='ne', padx=5, pady=7)
        label1.pack(fill='x', pady=15)
        label2.pack(fill='x', pady=5)
        label3.pack(fill='x', pady=7)
        right_frame.grid(row=0, column=1, padx=5)
        grid_frame.pack(padx=20, pady=7)

        if tutorial is True:
            checked = IntVar()
            cbtn = Checkbutton(help_pop, text='Do not show again', variable=checked)
            cbtn.pack(padx=20,pady=3)
            btn['command'] = lambda: close_help(help_pop, checked=checked.get())
            help_pop.protocol('WM_DELETE_WINDOW', lambda: self.close_help(help_pop, checked=checked.get()))

        btn.pack(padx=20, pady=10)
        help_pop.update()
        help_pop.geometry('{}x{}'.format(help_pop.winfo_width()+5, help_pop.winfo_height()+5))
        help_pop.mainloop()

    def close_help(self, window, checked=None):
        if checked == 1:
            c.setConfigNoHelp('Classify')
        window.destroy()

    def show_file_help(self):
        help_pop = tk.Tk()
        help_pop.title('Upload File Help')
        centerWindow(help_pop, 3.4, 2, 2.7, 2)

        # Top frame
        topFrame = Frame(help_pop)
        img_tr = PhotoImage(file='train_ds.png')
        img_te = PhotoImage(file='test_ds.png')
        label_img_tr = Label(topFrame, image=img_tr)
        label_img_te = Label(topFrame, image=img_te)
        label_train = Label(topFrame, text='Create Model Dataset')
        label_test = Label(topFrame, text='Excel File')
        label_img_tr.grid(row=0, column=0, padx=20, pady=5)
        label_img_te.grid(row=0, column=1, padx=20, pady=5)
        label_train.grid(row=1, column=0, padx=20, pady=5)
        label_test.grid(row=1, column=1, padx=20, pady=5)

        # Bottom frame
        bottomFrame = Frame(help_pop)
        grid_frame = Frame(bottomFrame)
        icon = Label(grid_frame, image="::tk::icons::question")
        label_desc = ttk.Label(grid_frame, text=('**NOTE** - The Excel file to be uploaded must have:' \
                                                 + '\n\n1) The SAME FEATURES as the create model dataset.' \
                                                 + '\n\n2) The SAME ORDER of features as the create model dataset.' \
                                                 + '\n\n3) The feature values must be of the SAME DATA TYPE as the create model dataset.'))
        btn = ttk.Button(bottomFrame, text='OK', command=help_pop.destroy)
        icon.grid(row=0, column=0, padx=5, pady=3, sticky='ne')
        label_desc.grid(row=0, column=1, padx=5, pady=10)
        grid_frame.pack()
        btn.pack(padx=20, pady=10)

        # Pack both frames
        topFrame.pack(pady=10)
        bottomFrame.pack(pady=7)
        help_pop.update()
        help_pop.mainloop()


    # Popup methods
    def show_classifyingVal_popup(self):
        classify_pop = tk.Tk()
        classify_pop.title('Info')
        centerWindow(classify_pop,2,2,1.85,2)

        grid_frame = Frame(classify_pop)
        icon = Label(grid_frame, image='::tk::icons::information')
        label = Label(grid_frame, text='Classifying species...      ')
        icon.grid(row=0, column=0, padx=5)
        label.grid(row=0, column=1)
        grid_frame.pack(padx=15, pady=17)
        classify_pop.after(1500,classify_pop.destroy)
        classify_pop.mainloop()

    def show_saveResult_popup(self):
        root = tk.Tk()
        root.withdraw()
        save_path = filedialog.asksaveasfilename(initialdir="/", title="Save file", filetypes=(("Excel Files", "*.xlsx"), ("all files", "*.*")),
                                                 defaultextension='.xlsx')
        root.destroy()
        return save_path

    def show_classifyFile_popup(self, file_path, save_path):
        # Global var for check/cancel_p_classify()
        global classifyFile_pop
        global pbar_classify
        global p_classify

        classifyFile_pop = tk.Tk()
        classifyFile_pop.title('Info')
        centerWindow(classifyFile_pop, 2.05, 2, 1.85, 2)
        classifyFile_pop.protocol('WM_DELETE_WINDOW', lambda:self.show_cantInterrupt())

        p_classify = multiprocessing.Process(target=c.classify, args=[file_path, save_path])
        grid_frame = Frame(classifyFile_pop)
        right_frame = Frame(grid_frame)
        icon = Label(grid_frame, image='::tk::icons::information')
        label = Label(right_frame, text='Classifying all data...')
        pbar_classify = ttk.Progressbar(right_frame, mode='indeterminate', length=105)

        icon.grid(row=0, column=0, sticky='nsew')
        label.pack()
        pbar_classify.pack(pady=8)
        right_frame.grid(row=0, column=1, padx=10)
        grid_frame.pack(pady=17)
        classifyFile_pop.update()

        classifyFile_pop.geometry('{}x{}'.format(classifyFile_pop.winfo_width()+35,classifyFile_pop.winfo_height()))
        pbar_classify.start()
        p_classify.start()
        classifyFile_pop.after(20, self.check_p_classify)
        classifyFile_pop.mainloop()

    def check_p_classify(self):
        if p_classify.is_alive():
            classifyFile_pop.after(20, self.check_p_classify)
        else:
            pbar_classify.stop()
            classifyFile_pop.destroy()

    def show_cantInterrupt(self):
        root = tk.Tk()
        root.withdraw()
        tk.messagebox.showwarning('Warning','The classification process can\'t be interrupted')
        root.destroy()

    def show_fileClassified_popup(self):
        root = tk.Tk()
        root.withdraw()
        tk.messagebox.showinfo('Results saved', 'Classification ended. Results saved as Excel file.')
        root.destroy()
        self.clear_values()


    # Button event methods
    def back_press(self):
        pass

    def input_press(self):
        f, f_vals = c.getFeatureInfo()
        entry = {}
        combobox = {}

        inputPop = tk.Tk()
        inputPop.title('Input Feature Values')
        centerWindow(inputPop,2.1,2,2,2)

        frame = Frame(inputPop)
        row = 0
        col = 0
        for feature in f:
            lbl = ttk.Label(frame, text='{}:'.format(feature))
            lbl.grid(row=row, column=col, padx=7, pady=5, sticky='w')
            col += 1

            if feature not in f_vals:  # An entry
                e = Entry(frame, font='DejaVuSans 10', width=7)
                e.grid(row=row, column=col, padx=7, pady=5, sticky='w')

                # If already have saved value
                if self.input_dict:
                    e.insert(0,self.input_dict[feature])
                entry[feature] = e

            else:  # A combobox
                longest_val = max(f_vals[feature], key=lambda k: len(k))
                cmb = ttk.Combobox(frame, values=f_vals[feature], justify=tk.CENTER, width=len(longest_val) + 3)

                # If already have saved value
                if self.input_dict:
                    for key in self.input_dict:
                        if feature in key:
                            # Example: if input_dict[f_'abc'] == 'abc'
                            if self.input_dict[key] == key[key.rfind('_')+1:]:
                                selected_val = key[key.rfind('_')+1:]
                                cmb.set(selected_val)
                else:
                    cmb.set(cmb['values'][0])
                cmb.grid(row=row, column=col, padx=7, pady=5, sticky='w')
                combobox[feature] = cmb
            row += 1
            col = 0
        frame.pack(padx=15, pady=7)

        btn = ttk.Button(inputPop, text='OK', command=lambda: self.checkInput(inputPop,entry,combobox))
        btn.pack(padx=20, pady=10)
        inputPop.mainloop()

    def checkInput(self,window,entry,combobox):
        input_dict,check_result = c.checkInput(entry,combobox)
        if check_result == 1:
            window.destroy()
            self.input_dict = input_dict
            self.value_txt.text = '[Values saved!]'
        else:
            tk.messagebox.showerror('Invalid input','Please provide correct feature values.')

    def upload_press(self):
        root = tk.Tk()
        root.withdraw()
        fp = filedialog.askopenfilename()
        if fp != '':
            fileValid = c.checkClassifyFile(fp)
            if fileValid == 1:
                self.file_path.text = self.compress_file_path(file_path=fp)
                self.full_file_path = fp
            elif fileValid == -1:
                show_error_popup('Invalid File Format', 'Please upload an Excel(.xlsx) file.')
            elif fileValid == -2:
                show_error_popup('Invalid Features', 'Features provided does not match with the current model\'s. See HELP for more details.')
            elif fileValid == -3:
                show_error_popup('Invalid Feature Values', 'Feature values provided either have invalid data type or does not match with the '
                                +'current model\'s. See HELP for more details.')
        root.destroy()

    def compress_file_path(self, file_path):
        folder_count = 0
        for i in range(len(file_path) - 1, -1, -1):
            if file_path[i] == '/':
                if folder_count == 1:
                    file_path = '~' + file_path[i:]
                    break
                else:
                    folder_count += 1
        return file_path

    def classify_press(self):
        # Input values OK
        if self.input_dict:
            result = c.classifySingle(self.input_dict.copy())
            self.show_classifyingVal_popup()
            self.showResultWindow(result)

        # Input values INVALID
        else:
            # File chosen
            if self.file_path.text != self.default_file_path:
                save_path = self.show_saveResult_popup()
                if save_path != '':
                    self.show_classifyFile_popup(self.full_file_path, save_path)
                    self.show_fileClassified_popup()
            # No file chosen
            else:
                show_error_popup('Error', 'Please provide correct feature values or upload an Excel(.xlsx) file.')

    def showResultWindow(self,result):
        resultPop = tk.Tk()
        resultPop.title('Result')
        resultPop.protocol('WM_DELETE_WINDOW', lambda: self.closeResult(resultPop))
        centerWindow(resultPop,3,2,2.7,2)

        save_btn = ttk.Button(resultPop, text='Save Result', command=self.save_press)
        mid_frame = Frame(resultPop)
        label1 = ttk.Label(mid_frame, text='Feature Information')
        label2 = ttk.Label(mid_frame, text='Classification Result')
        entry1 = tk.scrolledtext.ScrolledText(mid_frame, height=15, width=35)
        entry2 = tk.scrolledtext.ScrolledText(mid_frame, height=15, width=35)
        close_btn = ttk.Button(resultPop, text='Close', command=lambda: self.closeResult(resultPop))

        # Write f_vals on left entry
        f_vals_lines = '  ===== Feature Information =====\n\n'
        for f in self.input_dict:
            # Numerical vals
            try:
                float(self.input_dict[f])
                f_vals_lines += '{}: {}\n\n'.format(f, self.input_dict[f])
            # Categorical vals
            except ValueError:
                if self.input_dict[f] == f[f.rfind('_')+1:]:
                    f_vals_lines += '{}: {}\n\n'.format(f[:f.rfind('_')], self.input_dict[f])
        entry1.insert(INSERT, f_vals_lines)

        # Write result on right entry
        result_lines = ' ===== Classification Result =====\n\n'
        for species in result:
            result_lines += '{}: {:.2f}%\n\n'.format(species, result[species] * 100)
        entry2.insert(INSERT, result_lines)

        save_btn.pack(padx=20, pady=15)
        label1.grid(row=0, column=0, padx=10)
        label2.grid(row=0, column=1, padx=10)
        entry1.grid(row=1, column=0, padx=15, pady=5, sticky='w')
        entry2.grid(row=1, column=1, padx=15, pady=5, sticky='e')
        mid_frame.pack(padx=20)
        close_btn.pack(padx=20, pady=15)
        resultPop.mainloop()

    def closeResult(self,window):
        self.clear_values()
        window.destroy()

    def save_press(self):
        # Ask for path to save
        root = tk.Tk()
        root.withdraw()
        save_path = filedialog.asksaveasfilename(initialdir="/", title="Save file", filetypes=(("Excel Files", "*.xlsx"), ("all files", "*.*")),
                                                 defaultextension='.xlsx')
        root.destroy()

        # Export result as Excel & move to classify screen
        if save_path != '':
            c.exportSingleToExcel(save_path)
            self.show_save_popup()

    def show_save_popup(self):
        root = tk.Tk()
        root.withdraw()
        tk.messagebox.showinfo('Result saved', 'Classification result saved as Excel file.')
        root.destroy()

    def clear_values(self):
        self.input_dict = {}
        self.value_txt.text = self.default_value_txt
        self.file_path.text = self.default_file_path
