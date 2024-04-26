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
def addItem():
    addToMenu = load_menu('menu.json')
    print('What item do you want to add?\n')
    addedItem = input('->')
    print('What is the price of the item?\n')
    itemPrice = input('->')
    print('What is the quantity of the item?\n')
    itemQuantity = input('->')
    addedItemJSON = add_item_to_json('menu.json',addedItem,itemPrice,itemQuantity)
    print('Item added successfuly!')
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
            k=data.split(',')
            print('meow')
            if k[0] == 'Customer':
                print('hanzo')
                menu = load_menu('menu.json')
                print('d7man')
                menu = pickle.dumps(menu)
                print('fares 3mkm')
                conn.sendall(menu)
                print('3ziz')
            elif k[0] == 'Owner':
                if k[1]=='admin' and k[2]=='admin':
                    print('Hello dear Owner of Networant!')
                    print('Tell me what do you want to do?')
                    print('1- Add items to the menu\n2- Modify prices or quantity')
                    selection = input('->')
                    if selection == '1':
                        addItem()
                    elif selection == '2':
                        modifyItem()
                else:
                    print('\033[1;31;40m Username or password is incorrect.')
            else:
                print('howowow')

    except:
        print("\033[1;31;40m Error on server side")

if __name__ == '__main__':
    main()