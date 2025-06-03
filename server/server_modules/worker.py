import threading
from .utils import *

class Worker:
    def __init__(self,client_socket,client_adress,handler,notifier,notifications,capacity):
        self.client_socket = client_socket
        self.client_adress = client_adress
        self.handler = handler
        self.notifier = notifier
        self.notifications = notifications
        self.capacity = capacity
    
    def run(self):
            message = self.client_socket.recv(31457280)  
            print(self.client_socket)
            print(self.client_adress)
            print(message)
            hint,response = self.handler.handle(message.decode('utf_8').split(" "),self.client_adress[0],self.client_adress[1])
            print(response)
            self.client_socket.send(response)
            self.client_socket.close()
            
            if hint != "":
                if(hint != 'reload'):
                    addNotifications(hint,self.notifications,self.capacity)
                self.notifier.notify()
    
    def handleRequest(self):
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()