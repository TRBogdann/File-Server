from .database import *
from .user import *
from .file_manager import *
import os

def getUsername(adress,port,connections):
    for it in connections:
        if it.adress == adress and it.port == port:
                return it.username
    
    return "unk"

def adressExists(adress,port,connections):
    for it in connections:
        if it.adress == adress and it.port == port:
            return True
    
    return False

def unknownRequest():
    return "","err Unknown Command".encode("utf-8")


def badRequest():
    return "","err Bad Request".encode('utf-8')

def logIn(username,password,adress,port,listen_port,connections,db):
    if not db.userExists(username) or not db.checkPassword(username,password):
        return "","err Username or Password is Incorrect".encode('utf-8')
    
    for it in connections:
        if it.username == username:
            return "reload","err This User is already connected".encode('utf-8')
    
    connections.append(User(adress,port,listen_port,username))
    
    return f"{username} Connected",'ok Connected'.encode('utf-8')
    
    
def signUp(username,password,db):
    if db.userExists(username):
        return "","err Username Exits".encode('utf-8')
    
    db.insertUser(username,password)
    return "reload","ok User Created".encode('utf-8')

    
def sendFiles(adress,port,connections,filemanager):
    if not adressExists(adress,port,connections):
        return "","err User Not Logged In".encode('utf-8')

    
    return "",filemanager.getFilenames()
    
def sendPermissions(adress,port,connections,permissions):
    
    if not adressExists(adress,port,connections):
        return "","err User Not Logged In".encode('utf-8')
    
    edit = 1 if permissions[0] else 0 
    create = 1 if permissions[1] else 0 
    delete = 1 if permissions[2] else 0 
    
    message = f"ok {edit} {create} {delete}"
    return "",message.encode('utf-8')

def sendNotifications(adress,port,connections,notifications):
    if not adressExists(adress,port,connections):
        return "","err User Not Logged In".encode('utf-8')
    
    if len(notifications) == 0:
        return "","ok".encode('utf-8')
    
    message = "ok "
    for it in notifications:
        message += f'{it}\n'
    message = message[:-1]
    
    return "",message.encode('utf-8')

def sendFile(adress,port,connections,filemanager,filename):
    if not adressExists(adress,port,connections):
        return "","err User Not Logged In".encode('utf-8')

    filecontent = filemanager.getFile(filename)
    message = f"ok {filecontent}"
    
    return "",message.encode('utf-8')

def sendFileForEdit(adress,port,connections,permissions,filemanager,filename):
    if not adressExists(adress,port,connections):
        return "","err User Not Logged In".encode('utf-8')

    if permissions[0] == False:
        return "","err No Edit Permissions".encode('utf-8')

    if filemanager.isAssigned(filename):
        return "","err The file is being edited by another user".encode('utf-8')
    
    username = getUsername(adress,port,connections)
    print(username)
    filemanager.assignFile(filename,username)
    filecontent = filemanager.getFile(filename)
    message = f"ok {filecontent}"
    
    
    return f"{username} is editing '{filename}'",message.encode('utf-8')

# def reloadRequest(self):
#     return "reload".encode('utf-8')

def abort(adress,port,connections,filemanager,filename):
    username = getUsername(adress,port,connections)
    filemanager.freeUserFiles(username)
    return f"{username} aborted editing {filename}",'ok'.encode('utf-8')

def updateFile(adress,port,connections,filemanager,filename,filecontent):
    if not adressExists(adress,port,connections):
        return "","err User Not Logged In".encode('utf-8')
    
    username = getUsername(adress,port,connections)
    return filemanager.updateFile(filename,filecontent,username)

def createFile(adress,port,connections,filemanager,filename,filecontent):
    if not adressExists(adress,port,connections):
        return "","err User Not Logged In".encode('utf-8')
    
    username = getUsername(adress,port,connections)
    return filemanager.createFile(filename,filecontent,username)

def deleteFile(adress,port,connections,filemanager,filename):
    if not adressExists(adress,port,connections):
        return "","err User Not Logged In".encode('utf-8')
    
    username = getUsername(adress,port,connections)
    return filemanager.deleteFile(filename,username)

def logout(adress,port,connections,filemanager):
    username = getUsername(adress,port,connections)
    filemanager.freeUserFiles(username)
    for it in connections:
        if it.adress == adress and it.port == port:
            connections.remove(it)
            return f"{username} logged out","ok".encode('utf-8')
    return "unk logged out","ok".encode('utf-8')

class RequestHandler:
    def __init__(self,db,connections,notifications,filemanager):
        self.db = db
        self.connections = connections
        self.filemanager = filemanager
        self.notifications = notifications
    
    def handle(self,request,adress,port):
        if request[0] == 'login' :
            if len(request) != 4:
                return badRequest()
            
            return logIn(request[1],request[2],adress,port,request[3],self.connections,self.db)
        
        if request[0] == 'signup' :
            if len(request) != 3:
                return badRequest()
        
            return signUp(request[1],request[2],self.db)
        
        if request[0] == 'getfile' :
            if len(request) != 2:
                return badRequest()
            
            return sendFile(adress,port,self.connections,self.filemanager,request[1])
        
        if request[0] == 'edit' :
            if len(request) != 2:
                return badRequest()
            
            return sendFileForEdit(adress,port,self.connections,self.filemanager.permissions,self.filemanager,request[1])
        
        if request[0] == 'abort' :
            if len(request) != 2:
                return badRequest()
            return abort(adress,port,self.connections,self.filemanager,request[1])
        
        if request[0] == 'view' :    
            return sendFiles(adress,port,self.connections,self.filemanager)
        
        if request[0] == 'permissions' :            
            return sendPermissions(adress,port,self.connections,self.filemanager.permissions)
        
        if request[0] == 'notif':
            return sendNotifications(adress,port,self.connections,self.notifications)
        
        if request[0] == 'update':
            if len(request) < 2:
                return badRequest()
            
            rejoined = " ".join(request[1:])
            resplit = rejoined.split("|")
            if len(resplit) < 2:
                return badRequest()
            
            return updateFile(adress,port,self.connections,self.filemanager,resplit[0],resplit[1])   
        
        if request[0] == 'create':
            if len(request) < 2:
                return badRequest()
            
            rejoined = " ".join(request[1:])
            resplit = rejoined.split("|")
            if len(resplit) < 2:
                return badRequest()
            
            return createFile(adress,port,self.connections,self.filemanager,resplit[0],resplit[1])   
        
        if request[0] == 'delete' :
            if len(request) != 2:
                return badRequest()
            
            return deleteFile(adress,port,self.connections,self.filemanager,request[1])
        
        if request[0] == 'logout':
            return logout(adress,port,self.connections,self.filemanager)
        
        return unknownRequest() 