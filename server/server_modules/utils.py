
def getResult(text):
    if text == 'n' or text == 'N':
        return -1
    
    if text == 'y' or text == 'Y':
        return 1
    
    return 0

def createPermissions():
    edit_permission = False
    create_permission = False
    delete_permission = False

    res = 0
    while res == 0: 
        res = -1
        res = getResult(input("Do you want to grant edit permission to users? [y/n]\n"))
        if res == 0:
            print("Unknown Response , Response can be one of y,Y,n,N")
        
        if res == 1:
            edit_permission = True
    
    res = 0
    while res == 0: 
        res = -1
        res = getResult(input("Do you want to grant create permission to users? [y/n]\n"))
        if res == 0:
            print("Unknown Response , Response can be one of y,Y,n,N")
        
        if res == 1:
            create_permission = True
                
    res = 0        
    while res == 0: 
        res = -1
        res = getResult(input("Do you want to grant delete permission to users? [y/n]\n"))
        if res == 0:
            print("Unknown Response , Response can be one of y,Y,n,N")
        
        if res == 1:
            delete_permission = True
            
        return [edit_permission,create_permission,delete_permission]
    
def addNotifications(new_notif,notifications,capacity):
    if len(notifications) >= capacity:
        notifications = notifications[1:]
    
    notifications.append(new_notif)