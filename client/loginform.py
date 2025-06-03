from tkinter import *
from tkinter import messagebox
from request import RequestBuilder
from manager import ConnectionManager

class LogInForm:
    def __init__(self,root,callback_login,connectionManager:ConnectionManager):
        self.callback_login = callback_login
        self.requestBuilder = RequestBuilder()
        self.connectionManager = connectionManager
        
        frame = Frame(root, bg="white", bd=2, relief=SOLID)
        frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(frame, text="Login", font=("Arial", 20, "bold"), bg="white", pady=10).grid(row=0, column=0, columnspan=2)

        Label(frame, text="Username:", font=("Arial", 12), bg="white").grid(row=1, column=0, sticky=E, padx=10, pady=10)
        self.username_entry = Entry(frame, font=("Arial", 12), width=30, bd=2, relief=GROOVE)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)

        Label(frame, text="Password:", font=("Arial", 12), bg="white").grid(row=2, column=0, sticky=E, padx=10, pady=10)
        self.password_entry = Entry(frame, font=("Arial", 12), width=30, bd=2, relief=GROOVE, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)

        # Button actions
        Button(frame, text="Log In", font=("Arial", 12), width=15, bg="#0078D7", fg="white",
            command=self.validate_login).grid(row=3, column=0, padx=10, pady=20)

        Button(frame, text="Sign Up", font=("Arial", 12), width=15, bg="#d9534f", fg="white",
            command=self.validate_signup).grid(row=3, column=1, padx=10, pady=20)

        self.username_entry.focus_set()

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            response = self.connectionManager.sendRequest(self.requestBuilder.logInRequest(
                username=username,
                password=password,
                listen_port=self.connectionManager.broadcast_adress[1]
            )) 
            
            response = response.decode('utf-8')
            
            if response.split(" ")[0] == 'ok':
                self.callback_login()
            else:
                messagebox.showerror('err',response)
        else:
            messagebox.showerror("The fields cannot be left empty")

    def clear_fields(self):
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
    
    def validate_signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            response = self.connectionManager.sendRequest(self.requestBuilder.signUpRequest(
                username=username,
                password=password   
            ))
            
            response = response.decode('utf-8')
            
            if response.split(" ")[0] == 'ok':
                messagebox.showerror("Ok","Account created")
            else:
                messagebox.showerror('err',response)
        else:
            messagebox.showerror("The fields cannot be left empty")