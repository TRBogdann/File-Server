import bcrypt

class Encryptor:
    def encryptPassword(self,password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def isCorrectPassword(self,passhash,password):
        return bcrypt.checkpw(password.encode('utf-8'),passhash.encode('utf-8'))
    