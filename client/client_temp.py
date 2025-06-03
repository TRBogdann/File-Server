import socket
from request import RequestBuilder
from manager import ConnectionManager

requestBuilder = RequestBuilder()
connectionManager = ConnectionManager(('127.0.0.1',2020))

response = connectionManager.sendRequest(requestBuilder.logInRequest(
    username='user1234',
    password='hash123',
    listen_port=connectionManager.getListenSocket().getsockname()[1]
    ))
print(response)


response = connectionManager.sendRequest(requestBuilder.viewFilesRequest())
print(response)

response = connectionManager.sendRequest(requestBuilder.getPermissionsRequest())
print(response)