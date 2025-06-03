from .file_manager import *
import threading
import socket
import time

class Notifier:
    def __init__(self,connections,fileManager):
        self.connections = connections
        self.fileManager = fileManager
        self.wait = False
        self.count = 0
    

    def notify(self):
        self.count += 1
        
    def sendAll(self):
        self.wait = True
        remove_list = []
        for user in self.connections:
            try:

                sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sender.settimeout(1.0)
                sender.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sender.sendto("reload".encode("utf-8"), (user.adress, int(user.broadcast)))
                sender.close()
                print(f"Sent message to {user.username}")
            except Exception as e:
                print(f"Failed to send to {user.username}: {e}")
                remove_list.append(user)
        
        for user in remove_list:
            self.fileManager.freeUserFiles(user.username)
            self.connections.remove(user)
        self.wait = False
    
    def startNotifier(self):
        def runable():
            while True:
                if not self.wait and self.count>0:
                    self.sendAll()
                    self.count-=1
                time.sleep(0.5)
        
        thread = threading.Thread(target=runable, daemon=True)
        thread.start()
        
        
        