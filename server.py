import socket
import json
import pickle
import time
import sys
port = 12388
ip = 'localhost'


def load_menu(file_path):
    with open(file_path, 'r') as file:
        menu_data = json.load(file)
    return menu_data
def add_item_to_json(file_path, item_name, item_price, item_quantity):
 
    data =load_menu('menu.json')
    data[item_name] = {
        "price": int(item_price),
        "quantity": int(item_quantity)
    }

    update_menu(file_path,data)

def modifyItem(conn):
    menu_data = load_menu('menu.json')
    modifiedItem = conn.recv(1024).decode() 
    if modifiedItem in menu_data:
        ACK = '1'
        newPrice = conn.recv(1024).decode()
        newQuantity = conn.recv(1024).decode()
        menu_data[modifiedItem]['price'] = int(newPrice)
        menu_data[modifiedItem]['quantity'] = int(newQuantity)

        update_menu('menu.json',menu_data)
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
        ack='1'
        del menu[deletedItem]
        update_menu('menu.json',menu)
        conn.sendall(ack.encode())
    else:
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

                Order = conn.recv(1024).decode()
                print(Order)
                Quantity = conn.recv(1024).decode()
                ListOrders = Order.split(',')
                ListQuantity = Quantity.split(',')
                print(ListOrders)
                ListOrders.remove('')
                ListQuantity.remove('')

                print("ant 3la algadh")
                totalBill = 0
                print("k1")
                menu = load_menu('menu.json')
                Diclined = False
                conn.sendall(b'Loop')
                for i in range(0, len(ListOrders)):
                    Diclined = False
                    if int(menu[ListOrders[i]]["quantity"]) < int(ListQuantity[i]):
                        Diclined = True
                        if Diclined:
                            conn.sendall(b'0')
                            time.sleep(0.2)
                            conn.sendall(str(ListOrders[i]).encode())
                            conn.sendall(str(menu[ListOrders[i]]["quantity"]).encode())
                            print('ddd')

                            ans = conn.recv(1024).decode()

                            if ans == 'y':
                                modQuantity = conn.recv(1024).decode()
                                ListQuantity[i] = modQuantity
                                totalBill += (int(ListQuantity[i]) * int(menu[ListOrders[i]]['price']))
                            elif ans == 'n':
                                ListQuantity[i] = 0
                    else:
                        totalBill += (int(ListQuantity[i]) * int(menu[ListOrders[i]]['price']))
                        conn.sendall(b'1')

                time.sleep(0.2)
                conn.sendall(b'finish')
                conn.sendall(str(totalBill).encode())

                ACK = conn.recv(1024).decode()
                if ACK == '1':
                    for i in range(len(ListOrders)):
                        NewQuantity = int(menu[ListOrders[i]]["quantity"]) - int(ListQuantity[i])
                        menu[ListOrders[i]]["quantity"] = NewQuantity
                    conn.sendall(b'1')
                    update_menu('menu.json',menu)
                elif ACK == '0':
                    main()

               
            elif data == 'Owner':
                username = conn.recv(1024).decode()
                password = conn.recv(1024).decode()
                if username =='admin' and password =='admin':
                    
                    while True:
                        ACK = '1'
                        conn.sendall(ACK.encode())
                        selection = conn.recv(1024).decode()
                        if selection == '1':
                            addItem(conn)
                        elif selection == '2':
                            modifyItem(conn)
                        elif selection == '3':
                            deleteItem(conn)
                        elif selection == '4':
                            break
                else:
                    ACK = '0'
                    conn.sendall(ACK.encode())
            elif data == 'Exit':
                sys.exit()
            
            else:
                ACK = '-1'
                conn.sendall(ACK.encode())
            

    except Exception as e:
        print("\033[1;31;40m Error on server side",str(e))

if __name__ == '__main__':
    main()