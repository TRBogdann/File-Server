from server_modules.database import UserDataBase
from server_modules.user import User
from server_modules import utils
from server_modules.functionality import RequestHandler
from server_modules.file_manager import FileManager
from server_modules.notifier import Notifier
from server_modules.worker import Worker
import socket
import os
import json

#Server Config

#1. Users
home = os.getenv('HOME')
connections = []
capacity = 10 
notifications = []
db = UserDataBase(home+'/.file-server/users.db')
edit_permission,create_permission,delete_permission = utils.createPermissions()

#2. Folder
folder = home+'/.file-server/files'
fileManager = FileManager(folder,[edit_permission ,create_permission, delete_permission])

#2. Handler
handler = RequestHandler(db,connections,notifications,fileManager)

#3 Notifier
notifier = Notifier(connections,fileManager)
notifier.startNotifier()

#Socket
config  = home+"/.config/FileServer/config.json"
settings = json.load(open(config))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((settings["host"],settings["port"]))
server.listen(settings["connection_limit"])

print("Server started")
while True:
    client_socket,client_adress = server.accept()
    worker = Worker(client_socket,client_adress,handler,notifier,notifications,capacity)
    worker.handleRequest()

