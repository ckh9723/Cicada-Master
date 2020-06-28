# Kivy modules
from kivy.uix.floatlayout import FloatLayout

# Tkinter modules
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import tkinter.scrolledtext
from tkinter import filedialog

# Other & self-defined modules
import time
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

def show_createHelp(tutorial=False):
    help_pop = tk.Tk()
    help_pop.title('Create Model Help')
    centerWindow(help_pop, 2.55, 2, 2.8, 2)
    help_pop.protocol('WM_DELETE_WINDOW', lambda: close_help(help_pop))

    # Top Frame
    top_frame = Frame(help_pop)
    img_cr = PhotoImage(file='create_ds.png')
    label_img_cr = Label(top_frame, image=img_cr)
    label1 = Label(top_frame, text='Excel file')
    label_img_cr.pack(pady=10)
    label1.pack()

    # Bottom Frame
    btm_frame = Frame(help_pop)
    grid_frame = Frame(btm_frame)
    icon = Label(grid_frame, image="::tk::icons::question")
    label2 = ttk.Label(grid_frame, text='**NOTE** - The dataset uploaded must fulfill the following conditions:' \
                                        + '\n\n1) The column containing labels in the dataset MUST be at the last column.' \
                                        + '\n\n2) The dataset CANNOT contain any missing values. ')
    btn = ttk.Button(btm_frame, text='OK', command=help_pop.destroy)
    icon.grid(row=0, column=0, padx=5, sticky='ne')
    label2.grid(row=0, column=1, padx=5, pady=7)
    grid_frame.pack(pady=7)

    if tutorial is True:
        checked = IntVar()
        cbtn = Checkbutton(btm_frame, text='Do not show again', variable=checked)
        cbtn.pack(pady=8)
        btn.pack(pady=5)
        help_pop.protocol('WM_DELETE_WINDOW', lambda: close_help(help_pop, checked.get()))
    else:
        btn.pack(pady=5)

    # Pack both frames
    top_frame.pack(padx=20, pady=5)
    btm_frame.pack(padx=20, pady=5)
    help_pop.update()
    help_pop.geometry('{}x{}'.format(help_pop.winfo_width(), help_pop.winfo_height()+5))
    help_pop.mainloop()

def close_help(window,checked=None):
    if checked == 1:
        c.setConfigNoHelp('Create')
    window.destroy()



class Create_Screen(FloatLayout):
    # create_status = -1  # Status of create model process (1-Success, 0-Cancelled)

    # Help methods
    def show_createHelp(self,tutorial=False):
        help_pop = tk.Tk()
        help_pop.title('Create Model Help')
        centerWindow(help_pop, 2.55, 2, 2.7, 2)
        help_pop.protocol('WM_DELETE_WINDOW', lambda: self.close_help(help_pop))

        # Top Frame
        top_frame = Frame(help_pop)
        img_cr = PhotoImage(file='create_ds.png')
        label_img_cr = Label(top_frame, image=img_cr)
        label1 = Label(top_frame, text='Excel file')
        label_img_cr.pack(pady=10)
        label1.pack()

        # Bottom Frame
        btm_frame = Frame(help_pop)
        grid_frame = Frame(btm_frame)
        icon = Label(grid_frame, image="::tk::icons::question")
        label2 = ttk.Label(grid_frame, text='**NOTE** - The dataset uploaded must fulfill the following conditions:' \
                                            + '\n\n1) The column containing labels in the dataset MUST be at the last column.' \
                                            + '\n\n2) The dataset CANNOT contain any missing values. ')
        btn = ttk.Button(btm_frame, text='OK', command=help_pop.destroy)
        icon.grid(row=0, column=0, padx=5, sticky='ne')
        label2.grid(row=0, column=1, padx=5, pady=7)
        grid_frame.pack(pady=5)

        if tutorial is True:
            checked = IntVar()
            cbtn = Checkbutton(btm_frame, text='Do not show again', variable=checked)
            cbtn.pack()
            btn.pack(pady=3)
            help_pop.protocol('WM_DELETE_WINDOW', lambda: self.close_help(help_pop, checked.get()))
        else:
            btn.pack(pady=5)

        # Pack both frames
        top_frame.pack(padx=20, pady=5)
        btm_frame.pack(padx=20, pady=5)
        help_pop.update()
        help_pop.geometry('{}x{}'.format(help_pop.winfo_width(), help_pop.winfo_height()+5))
        help_pop.mainloop()

    def close_help(self, window, checked=None):
        if checked == 1:
            c.setConfigNoHelp('Create')
        window.destroy()


    # Pop-up methods
    def show_warnFeature(self,file_path):
        warn_pop = tk.Tk()
        warn_pop.title('Warning')
        centerWindow(warn_pop,2.4,2,2.2,2)

        top_frame = Frame(warn_pop)
        label = ttk.Label(top_frame, text='The model is designed to be built with the following features:')
        label2 = ttk.Label(top_frame, text='1) Echeme Duration\n' \
                                          +'2) Echeme Period\n' \
                                          +'3) Inter-Echeme Duration')
        label3 = ttk.Label(top_frame, text='The features in the uploaded file are different and might affect accuracy. \nProceed to build model?')
        checked = IntVar()
        cbtn = Checkbutton(top_frame, text='Do not show again', variable=checked)
        btn_frame = Frame(warn_pop)
        btn1 = ttk.Button(btn_frame, text='Yes', command=lambda: self.buildWarnFeature(warn_pop,file_path,checked))
        btn2 = ttk.Button(btn_frame, text='No', command=lambda: self.destroyWarnFeature(warn_pop,checked))

        label.pack(fill='x', padx=20, pady=10)
        label2.pack(fill='x', padx=20)
        label3.pack(fill='x', padx=20, pady=10)
        cbtn.pack(padx=20)
        top_frame.pack(pady=5)
        btn1.grid(row=0, column=0, padx=25, pady=10)
        btn2.grid(row=0, column=1, padx=25, pady=10)
        btn_frame.pack()
        warn_pop.mainloop()

    def buildWarnFeature(self,window,file_path,checked):
        if checked.get() == 1:
            c.setConfigNoHelp('CreateFeatureWarn')
        window.destroy()
        self.show_creatingPopup(file_path)

    def destroyWarnFeature(self,window,checked):
        if checked.get() == 1:
            c.setConfigNoHelp('CreateFeatureWarn')
        window.destroy()

    def show_warnCreate(self,file_path):
        warnCreate_pop = tk.Tk()
        warnCreate_pop.title('Create Model')
        centerWindow(warnCreate_pop,2.4,2,1.9,2)

        grid_frame = Frame(warnCreate_pop)
        btn_frame = Frame(warnCreate_pop)
        icon = Label(grid_frame, image='::tk::icons::question')
        label = ttk.Label(grid_frame, text='The time taken to create the model will vary depending on the size of \n ' \
                                           + 'the dataset and may take several minutes. Proceed to build model?')
        checked = IntVar()
        cmb = Checkbutton(warnCreate_pop, text='Do not show again', variable=checked)
        btn1 = ttk.Button(btn_frame, text='Yes', command=lambda: self.buildWarnCreate(warnCreate_pop,checked,file_path))
        btn2 = ttk.Button(btn_frame, text='No', command=lambda: self.destroyWarnCreate(warnCreate_pop,checked))

        icon.grid(row=0, column=0, padx=5)
        label.grid(row=0, column=1, padx=5)
        grid_frame.pack(padx=15, pady=10)
        cmb.pack()
        btn1.grid(row=0, column=0, padx=20)
        btn2.grid(row=0, column=1, padx=20)
        btn_frame.pack(pady=15)
        warnCreate_pop.mainloop()

    def buildWarnCreate(self,window,checked,file_path):
        if checked.get() == 1:
            c.setConfigNoHelp('CreateWarn')
        window.destroy()
        self.show_creatingPopup(file_path)

    def destroyWarnCreate(self,window,checked):
        if checked.get() == 1:
            c.setConfigNoHelp('CreateWarn')
        window.destroy()

    def show_creatingPopup(self,file_path):
        # Update status variable
        status = [1]

        creating_pop = tk.Tk()
        creating_pop.title("Creating Model")
        centerWindow(creating_pop, 2.1, 2, 1.9, 2)
        creating_pop.protocol('WM_DELETE_WINDOW', lambda:self.cancel_p_create(p_create,pbar_create))

        p_create = multiprocessing.Process(target=c.createModel, args=[file_path])
        grid_frame = Frame(creating_pop)
        right_frame = Frame(grid_frame)
        icon = Label(grid_frame, image='::tk::icons::information')
        label = Label(right_frame, text='Building classification model...')
        pbar_create = ttk.Progressbar(right_frame, mode='indeterminate', length=135)
        btn = ttk.Button(creating_pop, text='Cancel', command=lambda: self.cancel_p_create(p_create,pbar_create,status))

        icon.grid(row=0, column=0, padx=5, sticky='nsew')
        label.pack()
        pbar_create.pack(pady=7)
        right_frame.grid(row=0, column=1, padx=5)
        grid_frame.pack(padx=5, pady=10)
        btn.pack(pady=5)
        creating_pop.update()

        creating_pop.geometry('{}x{}'.format(creating_pop.winfo_width()+20, creating_pop.winfo_height()+5))
        pbar_create.start()
        p_create.start()
        creating_pop.after(20, lambda: self.check_p_create(creating_pop,pbar_create,p_create,file_path,status))
        creating_pop.mainloop()

    def check_p_create(self,window,pbar,p,file_path,status):
        if p.is_alive():
            window.after(20, lambda: self.check_p_create(window,pbar,p,file_path,status))
        else:
            if status[0] == 1:
                pbar.stop()
                window.destroy()
                self.show_createdPopup(file_path)
            else:
                window.destroy()
                time.sleep(0.2)
                root = tk.Tk()
                root.withdraw()
                tk.messagebox.showinfo('Info', 'Cancelled create model.')
                root.destroy()

    def cancel_p_create(self,p,pbar,status):
        ans = tk.messagebox.askquestion('Warning','All model creation progress will be lost. Proceed?')
        if ans == 'yes':
            p.terminate()
            pbar.stop()
            status[0] = 0

    def show_createdPopup(self,file_path=''):
        root = tk.Tk()
        root.withdraw()
        acc,n_feature,n_class = c.getTempDetails()
        ans = tk.messagebox.askquestion('Model Created','A model is created with the following details. Do you wish to keep the model?\n\n'\
                                       +'- Estimated Accuracy: {:.2f}%\n\n'.format(float(acc)*100)\
                                       +'- Features: {}\n\n'.format(n_feature)\
                                       +'- Classes: {}'.format(n_class))
        root.destroy()

        if ans == 'yes':
            self.show_fillPopup(file_path)
        elif ans == 'no':
            c.deleteModel('temp')
            root = tk.Tk()
            root.withdraw()
            tk.messagebox.showinfo('Info', 'Model discarded.')
            root.destroy()

    def show_fillPopup(self, file_path):
        fillPop = tk.Tk()
        fillPop.title('Fill Model Details')
        centerWindow(fillPop,2.3,2,2.3,2)
        fillPop.protocol('WM_DELETE_WINDOW', lambda: self.callback(fillPop))

        frame = Frame(fillPop)
        label1 = Label(frame, text='Model Name: ')
        label2 = Label(frame, text='Dataset: ')
        label3 = Label(frame, text='Description: ')
        entry1 = ttk.Entry(frame)
        entry2 = ttk.Entry(frame)
        entry3 = tk.scrolledtext.ScrolledText(frame, height=10, width=35)
        btn = ttk.Button(fillPop, text='OK', command=lambda: self.checkDetails(fillPop,[entry1.get(),entry2.get(),entry3.get(1.0,END)]))

        # Get dataset name & insert as default
        dataset_name = file_path.split('/')[-1]
        entry2.insert(0, dataset_name)

        label1.grid(sticky='W', row=0, column=0, pady=5)
        entry1.grid(sticky='W', row=0, column=1, pady=5)
        label2.grid(sticky='W', row=1, column=0, pady=5)
        entry2.grid(sticky='W', row=1, column=1, pady=5)
        label3.grid(sticky='NW', row=2, column=0, pady=5)
        entry3.grid(sticky='W', row=2, column=1, pady=5)
        frame.pack(padx=15, pady=5)
        btn.pack(padx=15, pady=10)
        fillPop.mainloop()

    def callback(self,window):
        root = tk.Tk()
        root.withdraw()
        ans = tk.messagebox.askquestion('Warning','Closing this window will discard the model. Exit anyways?')
        root.destroy()
        if ans == 'yes':
            c.deleteModel('temp')
            tk.messagebox.showinfo('Info', 'Model discarded.')
            window.destroy()

    def checkDetails(self,window,input_list):
        input_list = c.processInputDetails(input_list)
        name = input_list[0]
        dataset = input_list[1]
        description = input_list[2]

        if name == '' or dataset == '' or description == '':
            show_error_popup('Error','Please make sure no fields are empty.')
        else:
            check_result = c.checkName(name)
            if check_result == 1:
                c.saveModel(name,dataset,description)
                window.destroy()
                self.showSuccessPopup(name, dataset, description)
            elif check_result == -1:
                show_error_popup('Error','Model name already exist, please use another name.')

    def showSuccessPopup(self,name,dataset,description):
        # Format length of details
        details = [name,dataset,description]
        for i in range(len(details)):
            if len(details[i]) > 40:
                details[i] = details[i][:35]+'...'

        root = tk.Tk()
        root.withdraw()
        tk.messagebox.showinfo('Model Saved','Model successfully saved with the following details:\n\n'\
                              +'Model Name: {}\n\n'.format(details[0])\
                              +'Model Dataset: {}\n\n'.format(details[1])\
                              +'Description: {}'.format(details[2]))
        root.destroy()


    # Button press methods
    def back_press(self):
        pass

    def upload_press(self):
        root = tk.Tk()
        root.withdraw()
        fp = filedialog.askopenfilename()
        root.destroy()

        if fp != '':
            check_result = c.checkCreateFile(fp)

            if check_result == 0:  # Different features
                if c.getShowHelp('CreateFeatureWarn') == 'True':
                    self.show_warnFeature(file_path=fp)
            elif check_result == 1:
                root = tk.Tk()
                root.withdraw()
                ans = tk.messagebox.askquestion('Create Model', 'Do you wish to create a new model using \'{}\'?'.format(fp))
                root.destroy()
                if ans == 'yes':
                    if c.getShowHelp('CreateWarn') == 'True':
                        self.show_warnCreate(file_path=fp)
                    else:
                        self.show_creatingPopup(file_path=fp)

            elif check_result == -1:
                show_error_popup('Invalid File Format','Please upload an Excel(.xlsx) file.')
            elif check_result == -2:
                show_error_popup('Invalid Columns', 'There needs to be at least 2 columns of data')
            elif check_result == -3:
                show_error_popup('Invalid Values', 'There are missing values or data type inconsistencies.')
            elif check_result == -4:
                show_error_popup('Invalid Label Values', 'The labels are not categorical.')
            elif check_result == -5:
                show_error_popup('Invalid Label Values', 'There is only one label.')

