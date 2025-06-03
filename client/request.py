
class RequestBuilder:
    def logInRequest(self,username,password,listen_port):
        message = f"login {username} {password} {listen_port}"
        return message.encode('utf-8')
    
    def signUpRequest(self,username,password):
        message = f"signup {username} {password}"
        return message.encode('utf-8')
    
    def reloadRequest(self):
        return "reload".encode('utf-8')
    
    def viewFilesRequest(self):
        return "view".encode('utf-8')
    
    def getPermissionsRequest(self):
        return "permissions".encode('utf-8')
    
    def getNotificationsRequest(self):
        return "notif".encode('utf-8')
    
    def forceReloadRequest(self):
        return "reload".encode('utf-8')
    
    def editFile(self,filename):
        message = f"edit {filename}"
        return message.encode('utf-8')
    
    def viewFile(self,filename):
        message = f"getfile {filename}"
        return message.encode('utf-8')
    
    def createFile(self,filename,filecontent):
        message = f'create {filename}|{filecontent}'
        return message.encode('utf-8')
    
    def deleteFile(self,filename):
        message = f"delete {filename}"
        return message.encode('utf-8')
    
    def updateFile(self,filename,filecontent):
        message = f"update {filename}|{filecontent}"
        return message.encode('utf-8')
    
    def abortEdit(self,filename):
        message = f"abort {filename}"
        return message.encode('utf-8')
    
    def logOut(self):
        return "logout".encode('utf-8')