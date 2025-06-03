import os

class ServerFile:
    def __init__(self,filename):
        self.filename = filename
        self.assignedTo = None
        
    def assignTo(self,username):
        self.assignedTo = username
        
        

class FileManager():
    def __init__(self,folder,permissions):
        self.folder = folder
        self.files = []
        self.permissions = permissions
        filenames = [f for f in  os.listdir(folder)]
        for filename in filenames:
            self.files.append(ServerFile(filename))
            
    def isAssigned(self,filename):
        for it in self.files:
            if it.filename == filename:
                if it.assignedTo != None:
                    return True
                return False
        
        return True
    
    def getFilenames(self):
        result = "ok"
        for it in self.files:
            item = f" {it.filename}|{'N' if it.assignedTo == None else it.assignedTo}"
            result += item
        return result.encode('utf-8')
    
    def getFile(self,filename):
        filepath = os.path.join(self.folder,filename)
        with open(filepath, "rb") as f:
            return f.read().decode('utf-8')
        
    def updateFile(self,filename,filecontent,username):
        if not self.permissions[0]:
            return "","err No Edit Permissions".encode('utf-8')
        
        for it in self.files:
            if it.filename == filename:
                if it.assignedTo != username and it.assignedTo != None:
                    return "","err File Not Asssigned To User".encode('utf-8')
                
        filepath = os.path.join(self.folder,filename)
        with open(filepath, "w") as f:
            f.write(filecontent)
            
        return f"{username} edited {filename}",'ok File Updated'.encode('utf-8')
        
    def assignFile(self,filename,username):
        for it in self.files:
            if it.filename == filename:
                it.assignTo(username)
    
    def deassignFile(self,filename):
        for it in self.files:
            if it.filename == filename:
                it.assignTo(None)
        
    def freeUserFiles(self,username):
        for it in self.files:
            if it.assignedTo == username:
                it.assignTo(None)
    
    def createFile(self,filename,filecontent,username):
        if not self.permissions[1]:
            return "","err No Create Permissions".encode('utf-8')
        
        filepath = os.path.join(self.folder,filename)
        with open(filepath, "w") as f:
            f.write(filecontent)
        
        self.files.append(ServerFile(filename))
        return f"{username} created {filename}","ok File Created".encode('utf-8')
    
    def deleteFile(self,filename,username):
        if not self.permissions[2]:
            return "","err No Delete Permissions".encode('utf-8')
        
        for it in self.files:
            if it.filename == filename:
                if it.assignedTo != None:
                    return "","err Cannot delete assigned files".encode('utf-8')
                self.files.remove(it)
        
        if os.path.exists(os.path.join(self.folder,filename)):
            os.remove(os.path.join(self.folder,filename))
            
        return f"{username} deleted {filename}","ok File Removed".encode('utf-8')
        