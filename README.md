# Server-Client Text File Management System

## Initial Features

The server manages a list of text files from a host directory.

The client authenticates with a username and receives the list of text files, along with the username of the client currently editing each file.

Any authenticated client can request to view the content of a file, in which case the server sends them the latest version of that file from disk.

A client can request to take a file for editing if it is available. In this case, the server sends the file’s content to the client and notifies all other clients that the file is now being edited by the requesting client.

The client can update the file’s content by requesting the server to save the new version. In this case, the server updates the file’s content on disk with what it received from the client and notifies all clients who are currently viewing this file with the new content so they can refresh their displayed data.

The client can release the file from editing, in which case the server notifies all authenticated clients that the file is no longer being edited by the previous editor and is available for editing by others.

When a file is added to or deleted from the server, it notifies all authenticated clients about the name of the file affected by the operation so they can add or remove it from their local list of available files.
