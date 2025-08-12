import tkinter as tk
from tkinter import *
from tkinter import messagebox
from request import RequestBuilder
import os

class FileEditor:
    def __init__(self,root,filename,filecontent,mode,connectionmanager):
        self.root = root
        self.filename = filename
        self.filecontent = filecontent
        self.mode = mode
        self.connectionmanager = connectionmanager
        self.editor = None
        self.text_area = None
        self.request = RequestBuilder()
    
    def reload(self):
        response = self.connectionmanager.sendRequest(self.request.viewFile(self.filename))
        response = response.decode('utf-8')
        if response[0:2] == 'ok':
            self.text_area.config(state=tk.NORMAL)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, response[3:])
            self.text_area.config(state=tk.DISABLED)
            
        
    def save_file(self):
        if self.mode == 'edit':
            self.connectionmanager.sendRequest(self.request.updateFile(self.filename,self.text_area.get("1.0", "end-1c")))
        if self.mode == 'create':
            self.connectionmanager.sendRequest(self.request.createFile(self.filename,self.text_area.get("1.0", "end-1c")))
        
    def abort_edit(self):
        if self.mode == 'edit':
            self.connectionmanager.sendRequest(self.request.abortEdit(self.filename))
    
    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")


    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")


    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")


    def select_all(self):
        self.text_area.event_generate("<<SelectAll>>")


    def delete_last_char(self):
        current = self.text_area.get(1.0, END)
        self.text_area.delete("end-2c", END)
        
    def on_toplevel_close(self):
        if self.mode == 'view':
            self.connectionmanager.removeCallBack(self.reload)
        if self.mode == 'edit':
            self.connectionmanager.sendRequest(self.request.abortEdit(self.filename))
        self.editor.destroy()  
        self.root.deiconify()
        
    def about_notepad(self):
        messagebox.showinfo("About Editor", "Works")


    def about_commands(self):
        commands = """
    Under the File Menu:
    - 'Save' saves your file
    - 'Abort' cancels all modifications after the last save

    Under the Edit Menu:
    - 'Copy' copies the selected text to your clipboard
    - 'Cut' cuts the selected text and removes it from the text area
    - 'Paste' pastes the copied/cut text
    - 'Select All' selects the entire text
    - 'Delete' deletes the last character 
    """
        messagebox.showinfo(title="All commands", message=commands)
        
    def build_ui(self):
        self.root.withdraw()
        self.editor = Toplevel()
        self.editor.title(f"{self.filename} - Notepad")
        self.editor.geometry('1600x1000')
        icon = os.getenv('HOME') + '/.config/FileSharing/Notepad.png'
        icon_image = tk.PhotoImage(file=icon)
        self.editor.iconphoto(False, icon_image)
        self.editor.protocol("WM_DELETE_WINDOW", self.on_toplevel_close)

        self.editor.columnconfigure(0, weight=1)
        self.editor.rowconfigure(0, weight=1)
        
        self.text_area = Text(self.editor, font=("Times New Roman", 12))
        self.text_area.grid(sticky=NSEW)
        self.text_area.insert(tk.END,self.filecontent)

        scroller = Scrollbar(self.text_area, orient=VERTICAL)
        scroller.pack(side=RIGHT, fill=Y)
        scroller.config(command=self.text_area.yview)
        
        if self.mode == 'view':
            self.text_area.config(yscrollcommand=scroller.set,state=tk.DISABLED)
        else:
            self.text_area.config(yscrollcommand=scroller.set)
            
        menu_bar = Menu(self.editor)
        
        if self.mode != 'view':
            file_menu = Menu(menu_bar, tearoff=False, activebackground='DodgerBlue')
            file_menu.add_command(label="Save", command=self.save_file)
            menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = Menu(menu_bar, tearoff=False, activebackground='DodgerBlue')
        edit_menu.add_command(label='Copy', command=self.copy_text)
        if self.mode != 'view':
            edit_menu.add_command(label='Cut', command=self.cut_text)
            edit_menu.add_command(label='Paste', command=self.paste_text)
        edit_menu.add_separator()
        edit_menu.add_command(label='Select All', command=self.select_all)
        if self.mode != 'view':
            edit_menu.add_command(label='Delete', command=self.delete_last_char)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        
        help_menu = Menu(menu_bar, tearoff=False, activebackground='DodgerBlue')
        help_menu.add_command(label='About Notepad', command=self.about_notepad)
        help_menu.add_command(label='About Commands', command=self.about_commands)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        
        self.editor.config(menu=menu_bar)
        
        if self.mode == 'view':
            self.connectionmanager.addCallBack(self.reload)