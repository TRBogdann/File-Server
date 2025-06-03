import socket
import threading
import time

class ConnectionManager:
    def __init__(self,server_adress,broadcast_adress=None,sender_adress = None,allowed=None):
        self.server_adress = server_adress
        self.sender_adress = sender_adress
        self.broadcast_adress = broadcast_adress
        print(self.sender_adress)
        print(self.broadcast_adress)
        self.allowed = allowed
        self.callbacks = []
        
    def addCallBack(self,callback):
        self.callbacks.append(callback)
    
    def removeCallBack(self,callback):
        self.callbacks.remove(callback)
    
    def findFreePort(self,start_port=3030, end_port=8080, host='0.0.0.0', socket_type=socket.SOCK_STREAM):
        for port in range(start_port, end_port + 1):
            with socket.socket(socket.AF_INET, socket_type) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                try:
                    s.bind((host, port))
                    return port
                except OSError:
                    continue  

        return None  
    
    def getSenderSocket(self):
        sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sender.settimeout(100)
        if self.sender_adress == None:
            free_port = self.findFreePort()
            sender.bind(("0.0.0.0", free_port))
            self.sender_adress = sender.getsockname() 
        else: 
            sender.bind(self.sender_adress)
        
        return sender
    
    def getListenSocket(self):
        broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.broadcast_adress == None:
            free_port = self.findFreePort()
            broadcast.bind(("0.0.0.0", free_port))
            self.broadcast_adress = broadcast.getsockname() 
            print(free_port)
        else: 
            broadcast.bind(self.broadcast_adress)
        
        return broadcast
    
    def sendRequest(self,request):
        run = True
        it = 0
        while run:
            try:
                sender = self.getSenderSocket()
                sender.connect(self.server_adress)
                sender.send(request)
                response = sender.recv(31457280)
                sender.close()
                run = False
            except:
                print("Server is busy. Wait")
                time.sleep(0.5)
                run = True
        return response
    
    def isAllowed(self,client_adress):
        if self.allowed == None:
            return True
        
        for it in self.allowed:
            if it[0] == client_adress[0] and it[1] == client_adress[1]:
                return True
        return False
        
    def startBroadcast(self):
        def listen_loop():
            broadcast = self.getListenSocket()
            while True:
                message, client_address = broadcast.recvfrom(1024)
                
                for callback in self.callbacks:
                    callback()

        thread = threading.Thread(target=listen_loop, daemon=True)
        thread.start()