import socket
import pickle
port = 12388
ip = 'localhost'




def userInterface(sock):
    
    while True:
        print('\033[1;34;40m <#>    Welcome to Networant!')
        print('\033[1;37;40m<#> Please select who are you as shown below:')
        print('\033[1;33;40m<#> 1- Owner\n<#> 2- Customer\n<#> 3- Exit\n\033[1;37;40m ->', end= ' ')
        selection = input('->')
        if selection == '1':
            sock.sendall(b'Owner')
            ownerAuth(sock)
        elif selection == '2':
            sock.sendall(b'Customer')
            retrieveMenu(sock)
        elif selection == '3':
            sock.sendall(b'Exit')
            print('<#> Thanks for dealing with Networant, Goodbye!')
            break

def retrieveMenu(sock):
    data = sock.recv(1024)
    data = pickle.loads(data)
    for i,k in data.items():
        print(i,":",k['price'])

def addItem(sock):
    print('What item do you want to add?\n')
    addedItem = input('->')
    while not addedItem.isalpha():
        print('Invalid input! Please enter only letters.')
        addedItem = input('->')
    sock.sendall(addedItem.encode())

    print('What is the price of the item?\n')
    itemPrice = input('->')
    while not itemPrice.isdigit():
        print('Invalid input! Please enter only integers.')
        itemPrice = input('->')
    sock.sendall(itemPrice.encode())

    print('What is the quantity of the item?\n')
    itemQuantity = input('->')
    while not itemQuantity.isdigit():
        print('Invalid input! Please enter only integers.')
        itemQuantity = input('->')
    sock.sendall(itemQuantity.encode())
    print('Item added successfuly!')

def modifyItem(sock):
    print('What item do you want to modify?\n')
    modifiedItem = input('->')
    while not modifiedItem.isalpha():
        print('Invalid input! Please enter only letters.')
        modifiedItem = input('->')
    sock.sendall(modifiedItem.encode())

    print('What is the new price of the item?\n')
    newPrice = input('->')
    while not newPrice.isdigit():
        print('Invalid input! Please enter only integers.')
        newPrice = input('->')
    sock.sendall(newPrice.encode())

    print('What is the new quantity of the item?\n')
    newQuantity = input('->')
    while not newQuantity.isdigit():
        print('Invalid input! Please enter only integers.')
        newQuantity = input('->')
    sock.sendall(newQuantity.encode())
    ackClient = sock.recv(1024).decode()
    if ackClient == '1':
        print('Item modified successfully!')
    elif ackClient == '0':
        print('Something is wrong')

def ownerAuth(sock):
    try:
        print('Enter your username:')
        username = input('->')
        sock.sendall(username.encode())
        print('Enter your password:')
        password = input('->')
        sock.sendall(password.encode())
        ackClient = sock.recv(1024).decode()
        if ackClient == '1':
            print('Hello dear Owner of Networant!')
            print('Tell me what do you want to do?')
            print('1- Add items to the menu\n2- Modify prices or quantity')
            selection = input('->')
            sock.sendall(selection.encode())
            if selection == '1':
                addItem(sock)
            elif selection == '2':
                modifyItem(sock)
        elif ackClient == '0':
            print('Username or password is incorrect.')
    except Exception as e:
        print("Username or password is not correcttt.",str(e))

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('socket initiated')

    try:
        sock.connect((ip,port))
        print('socket connected')
        userInterface(sock)
    except Exception as e:
        print('Error on client side:', str(e))


if __name__ == '__main__':
    main()