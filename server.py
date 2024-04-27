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

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
def modifyItem():
    menu_data = load_menu('menu.json')
    print('What item do you want to modify?\n')
    modifiedItem = input('->')

    if modifiedItem in menu_data:
        print('What is the new price of the item?\n')
        newPrice = input('->')
        print('What is the new quantity of the item?\n')
        newQuantity = input('->')

        menu_data[modifiedItem]['price'] = newPrice
        menu_data[modifiedItem]['quantity'] = newQuantity

        with open('menu.json', 'w') as file:
            json.dump(menu_data, file)

        print('Item modified successfully!')
    else:
        print('Item not found in the menu.')
def addItem(conn):
    addedItem = conn.recv(1024).decode()
    itemPrice = conn.recv(1024).decode()
    itemQuantity = conn.recv(1024).decode()
    addedItemJSON = add_item_to_json('menu.json',addedItem,itemPrice,itemQuantity)
def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('socket initiated')

        sock.bind((ip,port))
        print('socket binded')

        sock.listen(5)
        print('socket now listening')

        conn, addr = sock.accept()
        while True:
            print('socket connected')
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
                        break
                    elif selection == '2':
                        modifyItem()
                else:
                    ACK = '0'
                    conn.sendall(ACK.encode())
                    print('\033[1;31;40m Username or password is incorrect.')
            elif data == 'Exit':
                break
            else:
                print('howowow')
            

    except:
        print("\033[1;31;40m Error on server side")

if __name__ == '__main__':
    main()