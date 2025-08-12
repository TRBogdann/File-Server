import os
from tkinter import *
from tkinter import messagebox
from loginform import LogInForm
from manager import ConnectionManager
from main_form import MainForm
import tkinter as tk
import json

    
class App:
    def __init__(self):
        folder_path = os.getenv('HOME')+"/.file-sharing/cache"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        config = os.getenv('HOME') + '/.config/FileSharing/config.json'
        icon = os.getenv('HOME') + '/.config/FileSharing/icon.png'
        settings = json.load(open(config))
        
        server_adress = settings["server_adress"]
        server_port = settings["server_port"]
        sender = settings["sender_port"]
        host = settings["host"]
        broadcast = settings["broadcast_port"]
        allowed = []
        for ports in settings["allowed_ports"]:
            allowed.append((server_adress,ports))
        
        self.connectionManager = ConnectionManager((server_adress,server_port),(host,broadcast),(host,sender),allowed)
        self.connectionManager.startBroadcast()
        self.root = Tk()
        self.root.title("Login - File-Server")
        self.root.geometry("1000x800")
        icon_image = tk.PhotoImage(file=icon)
        self.root.iconphoto(False, icon_image)
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        self.login = LogInForm(self.root,self.showMain,self.connectionManager)
        self.main = MainForm(self.root,self.connectionManager)
    
    def showMain(self):
        self.main.show()
        
    def start(self):
        self.root.mainloop()
        