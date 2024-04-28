import socket
import json
import pickle

port = 12388
ip = 'localhost'


def load_menu(file_path):
    with open(file_path, 'r') as file:
        menu_data = json.load(file)
    return menu_data
def add_item_to_json(file_path, item_name, item_price, item_quantity):
 
    data =load_menu('menu.json')
    data[item_name] = {
        "price": item_price,
        "quantity": item_quantity
    }

    update_menu(file_path,data)

def modifyItem(conn):
    menu_data = load_menu('menu.json')
    modifiedItem = conn.recv(1024).decode() 
    if modifiedItem in menu_data:
        ACK = '1'
        newPrice = conn.recv(1024).decode()
        newQuantity = conn.recv(1024).decode()
        menu_data[modifiedItem]['price'] = newPrice
        menu_data[modifiedItem]['quantity'] = newQuantity

        with open('menu.json', 'w') as file:
            json.dump(menu_data, file)
        conn.sendall(ACK.encode())
        
    else:
        ACK = '0'
        conn.sendall(ACK.encode())
def addItem(conn):
    addedItem = conn.recv(1024).decode()
    itemPrice = conn.recv(1024).decode()
    itemQuantity = conn.recv(1024).decode()
    add_item_to_json('menu.json',addedItem,itemPrice,itemQuantity)
def deleteItem(conn):
    menu = load_menu('menu.json')
    deletedItem = conn.recv(1024).decode()
    if deletedItem in menu:
        print('z8')
        ack='1'
        del menu[deletedItem]
        update_menu('menu.json',menu)
        conn.sendall(ack.encode())
    else:
        print('5ra')
        ack='0'
        conn.sendall(ack.encode())

def update_menu(file_path,data):
     with open(file_path, 'w') as file: 
         json.dump(data, file,indent=4)
def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('\033[1;35;40msocket initiated\u001b[0m')

        sock.bind((ip,port))
        print('\033[1;35;40msocket binded\u001b[0m')

        sock.listen(5)
        print('\033[1;35;40msocket now listening\u001b[0m')

        conn, addr = sock.accept()
        print('\033[1;35;40msocket connected\u001b[0m')
        while True:
            
            data = conn.recv(1024).decode()
            if data == 'Customer':
                menu = load_menu('menu.json')
                menu = pickle.dumps(menu)
                conn.sendall(menu)

               
            elif data == 'Owner':
                username = conn.recv(1024).decode()
                password = conn.recv(1024).decode()
                if username =='admin' and password =='admin':
                    ACK = '1'
                    conn.sendall(ACK.encode())
                    selection = conn.recv(1024).decode()
                    if selection == '1':
                        addItem(conn)
                    elif selection == '2':
                        modifyItem(conn)
                    elif selection == '3':
                        deleteItem(conn)
                else:
                    ACK = '0'
                    conn.sendall(ACK.encode())
                    print('\033[1;31;40m Username or password is incorrect.\u001b[0m\n')
            elif data == 'Exit':
                break
            else:
                ACK = '-1'
                conn.sendall(ACK.encode())
            

    except:
        print("\033[1;31;40m Error on server side")

if __name__ == '__main__':
    main()