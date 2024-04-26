import socket
import pickle
port = 12388
ip = 'localhost'




def userInterface(sock):
    print('\033[1;34;40m Welcome to Networant!')
    print('\033[1;37;40m Please select who are you as shown below:')
    print('1- Owner\n2- Customer\n', end= ' ')
    selection = input()
    if selection == '1':
        ownerAuth(sock)
    elif selection == '2':
        sock.sendall(b'Customer')
def ownerAuth(sock):
    try:
        print('Enter your username:')
        username = input()
        print('Enter your password:')
        password = input()
        sock.sendall(b'Owner')
    except:
        
def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('socket initiated')

    try:
        sock.connect((ip,port))
        print('socket connected')
        userInterface(sock)
        data = sock.recv(1024)
        data = pickle.loads(data)
        for i,k in data.items():
            print(i,":",k['price'])

            
    except:
        print('eroor on client side')
   

if __name__ == '__main__':
    main()