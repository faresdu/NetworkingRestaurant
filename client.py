import socket
import pickle
port = 12388
ip = 'localhost'

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('socket instantiated')

    try:
        sock.connect((ip,port))
        print('socket connected')
    except:
        print('eroor on client side')
    data = sock.recv(4096)
    data = pickle.loads(data)
    print(data)

if __name__ == '__main__':
    main()