import socket
import pickle
port = 12388
ip = 'localhost'

def userInterface(sock):
    print('\033[1;34;40m Welcome to Networant!')
    print('\033[1;37;40m Please select who are you as shown below:')
    selection = input('1- Owner\n2- Customer\n')
    if selection == 1:
        sock.sendall('Owner')
    elif selection == 2:
        sock.sendall('Customer')

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('socket instantiated')

    try:
        sock.connect((ip,port))
        print('socket connected')
        userInterface(sock)
        data = sock.recv(4096)
        data = pickle.loads(data)
    except:
        print('eroor on client side')
   

if __name__ == '__main__':
    main()