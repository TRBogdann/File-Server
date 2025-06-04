import os
from tkinter import *
from tkinter import messagebox
from loginform import LogInForm
from manager import ConnectionManager
from main_form import MainForm
import tkinter as tk

    
class App:
    def __init__(self,broadcast,sender):
        folder_path = "./temp"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        self.connectionManager = ConnectionManager(('0.0.0.0',2020),('0.0.0.0',broadcast),('0.0.0.0',sender),[('0.0.0.0',2021),('0.0.0.0',2022)])
        self.connectionManager.startBroadcast()
        self.root = Tk()
        self.root.title("Login - Notepad")
        self.root.geometry("1000x800")
        icon_image = tk.PhotoImage(file='./Notepad.png')
        self.root.iconphoto(False, icon_image)
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        self.login = LogInForm(self.root,self.showMain,self.connectionManager)
        self.main = MainForm(self.root,self.connectionManager)
    
    def showMain(self):
        self.main.show()
        
    def start(self):
        self.root.mainloop()
        