from server_modules.database import UserDataBase
from server_modules.user import User
from server_modules import utils
from server_modules.functionality import RequestHandler
from server_modules.file_manager import FileManager
from server_modules.notifier import Notifier
from server_modules.worker import Worker
import socket

#Server Config

#1. Users
connections = []
capacity = 10 
notifications = []
db = UserDataBase('users.db')
edit_permission,create_permission,delete_permission = utils.createPermissions()

#2. Folder
folder = './files'
fileManager = FileManager(folder,[edit_permission ,create_permission, delete_permission])

#2. Handler
handler = RequestHandler(db,connections,notifications,fileManager)

#3 Notifier

notifier = Notifier(connections,fileManager)
notifier.startNotifier()

#Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0",2020))
server.listen(20)

print("Server started")
while True:
    client_socket,client_adress = server.accept()
    worker = Worker(client_socket,client_adress,handler,notifier,notifications,capacity)
    worker.handleRequest()

