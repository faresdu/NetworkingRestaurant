import socket
import yaml
import pickle

port = 12388
ip = 'localhost'

    
def load_menu(file_path):
    with open(file_path, 'r') as file:
        menu_data = yaml.safe_load(file)
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
            data = conn.recv(4096)
            if data == 'Customer':
                menu = load_menu('menu.yml')
                menu = pickle.dumps(menu)
                conn.sendall(menu)
        
    except:
        print("eroorrrrrr on server side")
    finally:
        sock.close()
    

if __name__ == '__main__':
    main()

