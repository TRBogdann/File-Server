import sqlite3
from .encryptor import *

class UserDataBase:
    def __init__(self,location):
        self.connection = sqlite3.connect(location,check_same_thread=False)
        self.hasher = Encryptor()
        
        table = """ CREATE TABLE USERS (
            Username VARCHAR(255) NOT NULL UNIQUE,
            Passhash VARCHAR(255) NOT NULL
        ); """

        cursor_obj = self.connection.cursor()
        
        try:
            cursor_obj.execute(table)
        except:
            print("Table Users Exists")
        
        cursor_obj.close()
        
    def userExists(self,username):
        
        cursor_obj = self.connection.cursor()
        result  = cursor_obj.execute(f"SELECT COUNT(*) FROM USERS WHERE USERNAME = '{username}'")
        exists = False
        
        for i in result:
            exists = i[0] == 1 
        
        cursor_obj.close()
        return exists
    
    def insertUser(self,username,password):
        cursor_obj = self.connection.cursor()
        try:
            cursor_obj.execute(f"INSERT INTO USERS VALUES('{username}','{self.hasher.encryptPassword(password)}')")
            self.connection.commit()
        except: 
            print("User Exists")
        cursor_obj.close()
        
    def checkPassword(self,username,password):
        cursor_obj = self.connection.cursor()
        result = cursor_obj.execute(f"SELECT PASSHASH FROM USERS WHERE USERNAME = '{username}'")
        correct = False
        
        for i in result:
            correct =  self.hasher.isCorrectPassword(i[0],password)
            
        cursor_obj.close()
        return correct