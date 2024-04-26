import socket
import json
import pickle

port = 12388
ip = 'localhost'

    
def load_menu(file_path):
    with open(file_path, 'r') as file:
        menu_data = json.load(file)
    return menu_data

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('socket initiated')

        sock.bind((ip,port))
        print('socket binded')

        sock.listen(5)
        print('socket now listening')
        while True:
            conn, addr = sock.accept()
            print('socket connected')
            data = conn.recv(1024).decode()
            print(data)
            if data == 'Customer':
                menu = load_menu('menu.json')
                menu = pickle.dumps(menu)
                conn.sendall(menu)
            elif data == 'Owner':
                username = 'admin'
                password = 'admin'
                
                
                
        
    except:
        print("eroorrrrrr on server side")
    finally:
        sock.close()
    

if __name__ == '__main__':
    main()

