import tkinter as tk
from tkinter import messagebox, Toplevel
from request import RequestBuilder
from manager import ConnectionManager
from fileeditor import FileEditor

class MainForm:
    def __init__(self, root, connectionManager: ConnectionManager):
        self.connectionManager = connectionManager
        self.request = RequestBuilder()
        self.permissions = []
        self.root = root
        self.filenames = []
        self.assiged = []
        self.app_window = None
        self.notif_var = tk.StringVar()
        self.filename_var = tk.StringVar()  

    def on_edit(self, index):
        def handler():
            filename = self.filenames[index]
            response = self.connectionManager.sendRequest(self.request.editFile(filename))
            response = response.decode('utf-8')
            if response[0:2] == 'ok':
                editor = FileEditor(self.app_window, filename, response[3:], 'edit', self.connectionManager)
                editor.build_ui()
            else:
                messagebox.showerror("Error", response)
        return handler

    def on_view(self, index):
        def handler():
            filename = self.filenames[index]
            response = self.connectionManager.sendRequest(self.request.viewFile(filename))
            response = response.decode('utf-8')
            if response[0:2] == 'ok':
                editor = FileEditor(self.app_window, filename, response[3:], 'view', self.connectionManager)
                editor.build_ui()
            else:
                messagebox.showerror("Error", response)
        return handler

    def load(self):
        self.permissions = self.getPermissions()
        self.notif_var.set("")
        self.filenames = []
        self.assiged = []

        if self.app_window is not None:
            for widget in self.app_window.winfo_children():
                widget.destroy()

        files = self.connectionManager.sendRequest(self.request.viewFilesRequest()).decode('utf-8').split(" ")
        for i in range(1, len(files)):
            fileInfo = files[i].split('|')
            self.filenames.append(fileInfo[0])
            self.assiged.append("" if fileInfo[1] == 'N' else fileInfo[1])

        notifications = self.connectionManager.sendRequest(self.request.getNotificationsRequest()).decode('utf-8')
        if len(notifications) > 3:
            self.notif_var.set(notifications[3:])

        self.createListView()

        # Input field for new filename
        input_frame = tk.Frame(self.app_window)
        tk.Label(input_frame, text="New Filename:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Entry(input_frame, textvariable=self.filename_var, width=30).pack(side=tk.LEFT, padx=5)
        input_frame.pack(pady=5)

        # Buttons
        buttons_frame = tk.Frame(self.app_window)
        if self.permissions[1]:
            tk.Button(buttons_frame, text="Create", command=self.on_create, width=10).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(buttons_frame, text="Refresh", command=self.load, width=10).pack(side=tk.LEFT, padx=10)
        buttons_frame.pack()

        self.createNotificator()

    def createNotificator(self):
        notif_bar = tk.Label(self.app_window, textvariable=self.notif_var, relief=tk.SUNKEN,
                    anchor="w", bg="lightyellow", font=("Arial", 10))
        notif_bar.pack(fill="x", padx=5, pady=5)

    def createListView(self):
        header = tk.Frame(self.app_window)
        tk.Label(header, text="Filename", width=20, font=('Arial', 10, 'bold')).grid(row=0, column=0)
        tk.Label(header, text="Owner", width=20, font=('Arial', 10, 'bold')).grid(row=0, column=1)
        tk.Label(header, text="Action", width=20, font=('Arial', 10, 'bold')).grid(row=0, column=2, columnspan=2)
        header.pack(pady=5)

        list_frame = tk.Frame(self.app_window)
        for i in range(len(self.filenames)):
            tk.Label(list_frame, text=self.filenames[i], width=20).grid(row=i, column=0, padx=5, pady=2)
            tk.Label(list_frame, text=self.assiged[i], width=20).grid(row=i, column=1, padx=5, pady=2)
            tk.Button(list_frame, text="View", command=self.on_view(i)).grid(row=i, column=2, padx=5, pady=2)
            place = 3
            if self.permissions[0]:
                tk.Button(list_frame, text="Edit", command=self.on_edit(i)).grid(row=i, column=place, padx=5, pady=2)
                place += 1
            if self.permissions[2]:
                tk.Button(list_frame, text="Delete", command=self.on_delete(i)).grid(row=i, column=place, padx=5, pady=2)
        list_frame.pack()

    def on_toplevel_close(self):
        self.connectionManager.sendRequest(self.request.logOut())
        self.root.destroy()

    def on_create(self):
        filename = self.filename_var.get().strip()
        if not filename:
            messagebox.showerror("Error", "Please enter a filename.")
            return

        if filename in self.filenames:
            messagebox.showerror("Error", "File already exists")
            return

        
        editor = FileEditor(self.app_window, filename, "", 'create', self.connectionManager)
        editor.build_ui()
        
    def on_delete(self, index):
        def handler():
            filename = self.filenames[index]
            response = self.connectionManager.sendRequest(self.request.deleteFile(filename))
            response = response.decode('utf-8')
            if response[0:2] != 'ok':
                messagebox.showerror("Error", response)
            else:
                self.load()
        return handler

    def show(self):
        self.root.withdraw()
        self.app_window = Toplevel()
        self.app_window.title("Welcome")
        self.app_window.geometry("800x500")
        self.app_window.configure(bg="#e0f7fa")
        self.app_window.protocol("WM_DELETE_WINDOW", self.on_toplevel_close)
        self.load()
        self.connectionManager.addCallBack(self.load)

    def getPermissions(self):
        permissions = []
        response = self.connectionManager.sendRequest(self.request.getPermissionsRequest())
        response = response.decode('utf-8').split(" ")
        for i in range(1, 4):
            permissions.append(response[i] == '1')
        return permissions
