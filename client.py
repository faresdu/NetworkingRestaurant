import socket
import pickle
import sys
port = 12388
ip = 'localhost'




def userInterface(sock):
    flag = True
    for i in range(2):
        print('\033[1;34;40m <#> Welcome to Networant!')
        print('\033[1;37;40m <#> Please select who are you as shown below:')
        print('\033[1;33;40m <#> 1- Owner\n<#> 2- Customer\n<#> 3- Exit\n\033[1;37;40m ->', end= ' ')
        selection = ''
        selection = input('->')
        if selection == '1':
            ownerAuth(sock)
        elif selection == '2':
            sock.sendall(b'Customer,')
            retrieveMenu(sock)
        elif selection == '3':
            print('<#> Thanks for dealing with Networant, Goodbye!')
            sock.close()
            flag = False

def retrieveMenu(sock):
    data = sock.recv(1024)
    data = pickle.loads(data)
    for i,k in data.items():
        print(i,":",k['price'])
    

def ownerAuth(sock):
    try:
        print('Enter your username:')
        username = input()
        print('Enter your password:')
        password = input()
        x= ''
        x= 'Owner'+','+username + ',' + password
        sock.sendall(x.encode())
    except:
        print("Username or password is not correct.")

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