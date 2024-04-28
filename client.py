import socket
import pickle
port = 12388
ip = 'localhost'




def userInterface(sock):
    
    while True:
        print('\033[1;34;40m <#>    Welcome to Networant! \u001b[0m')
        print('\033[1;37;40m<#> Please select who are you as shown below:')
        print('\033[1;33;40m<+> 1- Owner\n<+> 2- Customer\n<+> 3- Exit\n\033[1;37;40m', end= ' ')
        selection = input('-> ')
        if selection == '1':
            sock.sendall(b'Owner')
            ownerAuth(sock)
        elif selection == '2':
            sock.sendall(b'Customer')
            customerAuth(sock)
        elif selection == '3':
            sock.sendall(b'Exit')
            print('\033[1;34;40m<#> Thanks for dealing with Networant, Goodbye!\u001b[0m')
            break
        else:
            print('\033[1;31;40m<-> Please enter a viable choice as shown above.\u001b[0m')


def addItem(sock):
    print('\033[1;33;40m<+> What item do you want to add?\u001b[0m\n')
    addedItem = input('->')
    while not addedItem.isalpha():
        print('\033[1;31;40m<#> Invalid input! Please enter only letters.\u001b[0m')
        addedItem = input('->')
    
    sock.sendall(addedItem.encode())
    print('\033[1;33;40m<+> What is the price of the item?\u001b[0m\n')
    itemPrice = input('->')
    while not itemPrice.isdigit():
        print('\033[1;31;40m<#> Invalid input! Please enter only integers.\u001b[0m')
        itemPrice = input('->')
    sock.sendall(itemPrice.encode())

    print('\033[1;33;40m<+> What is the quantity of the item?\u001b[0m\n')
    itemQuantity = input('->')
    while not itemQuantity.isdigit():
        print('\033[1;31;40m<#> Invalid input! Please enter only integers.\u001b[0m')
        itemQuantity = input('->')
    sock.sendall(itemQuantity.encode())
    print('<#> Item added successfuly!')\

def deleteItem(sock):
    print('What item do you want to delete?\n')
    deletedItem = input('->')
    sock.sendall(deletedItem.encode())
    respond = sock.recv(1024).decode()
    if respond=='1':
        print('item deleted successfully')
    elif respond=='0':
        print('item not found, nothing has been deleted')
        
def modifyItem(sock):
    print('\033[1;33;40m<+> What item do you want to modify?\u001b[0m\n')
    modifiedItem = input('->')
    while not modifiedItem.isalpha():
        print('\033[1;31;40m<#> Invalid input! Please enter only letters.\u001b[0m')
        modifiedItem = input('->')
    sock.sendall(modifiedItem.encode())

    print('\033[1;33;40m<+> What is the new price of the item?\u001b[0m\n')
    newPrice = input('->')
    while not newPrice.isdigit():
        print('\033[1;31;40m<#> Invalid input! Please enter only integers.\u001b[0m')
        newPrice = input('->')
    sock.sendall(newPrice.encode())

    print('\033[1;33;40m<+> What is the new quantity of the item?\u001b[0m\n')
    newQuantity = input('->')
    while not newQuantity.isdigit():
        print('\033[1;31;40m<#> Invalid input! Please enter only integers.\u001b[0m')
        newQuantity = input('->')
    sock.sendall(newQuantity.encode())
    ackClient = sock.recv(1024).decode()
    if ackClient == '1':
        print('\033[1;32;40m<#> Item modified successfully!\u001b[0m\n')
    elif ackClient == '0':
        print('\033[1;31;40m<-> Something is wrong\u001b[0m')

def customerAuth(sock):
    try:
        menuu=retrieveMenu(sock)

        loop = 'j'
        meals = ''
        quantity = ''
        match=True
        while loop != 'y':
            match = False
            print("enter your order: ", end=' ')
            cusOrder = input()
            for a in dict(menuu).keys():
                if a.lower() == cusOrder.lower():
                    match=True
            if match == False:
                print("There is no",cusOrder)
                continue

            print("Enter the quantity: ", end=' ')
            cusQuan = input()
            meals += cusOrder + ','
            quantity += cusQuan + ','
            print(meals)
            print("did you finish(y/n)", end=' ')
            loop = input()


        sock.sendall(meals.encode())
        sock.sendall(quantity.encode())
        # trace

        totalBill = sock.recv(1024).decode()
        if totalBill=='Diclined':
            diclinedOrder=sock.recv(1024).decode()
            diclinedOrderQuan = sock.recv(1024).decode()
            print("The", diclinedOrder, "Avaliable is" ,diclinedOrderQuan)
            print("Do you want to order this meal?(y/n): ", end="")
            ans = input()
            if ans =="y":
                print("How much Quantity: ", end="")
                anq = input()
                sock.sendall(b"y")
                sock.sendall(anq.encode())
                totalBill = sock.recv(1024).decode()
            elif ans=='n':
                sock.sendall(b'n')
                totalBill = sock.recv(1024).decode()



        print("your Bill is", totalBill, 'SAR')
        print("Do you confirm your order(y/n)", end=' ')
        confirm = input()
        if confirm == 'y':
            print("Put your address: ", end=' ')
            addr = input()
            sock.sendall(b'1')
            sock.sendall(addr.encode())
            ACK = sock.recv(1024).decode()
            if ACK == '1':
                print("Your order has been accepted by the restaurant")



    except:
        print('\033[1;31;40mThere is a problem.\u001b[0m',str(e))   
        

def retrieveMenu(sock):
    data = sock.recv(1024)
    data = pickle.loads(data)
    print('===============================')
    print('= meals             price(SAR)=')
    for i,k in data.items():
        print('=',i,end='')
        for l in range(0,18-len(str(i))):
            print(end=' ')
        print(k['price'],end='')
        for l in range(0, 10 - len(str(k['price']))):
            print(end=' ')

        print("=")
    print('===============================')
    return data

def ownerAuth(sock):
    try:
            print('\033[1;33;40m<+> Enter your username:\u001b[0m')
            username = input('->')
            sock.sendall(username.encode())
            print('\033[1;33;40m<+> Enter your password:\u001b[0m')
            password = input('->')
            sock.sendall(password.encode())
            ackClient = sock.recv(1024).decode()
            if ackClient == '1':
                print('\033[1;34;40m<#> Hello dear Owner of Networant!\u001b[0m')
                flag = False
                while not flag:
                    print('\033[1;37;40m<#> Tell me what do you want to do?\u001b[0m')
                    print("\033[1;33;40m<+> 1- Add items to the menu\n<+> 2- Modify prices or quantity\n<+> 3- Delete an item \n<+> 4- Exit owner's menu \u001b[0m")
                    selection = input('->')
                    sock.sendall(selection.encode())
                    if selection == '1':
                        addItem(sock)
                    elif selection == '2':
                        modifyItem(sock)
                    elif selection == '3':
                        deleteItem(sock)
                    elif selection == '4':
                        flag = True
                        break
            elif ackClient == '0':
                print('\033[1;31;40m<-> Username or password is incorrect.\u001b[0m')
    except Exception as e:
        print("\033[1;31;40m<->Username or password is not correct2.\u001b[0m",str(e))

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('\033[1;35;40m<#> socket initiated')

    try:
        sock.connect((ip,port))
        print('\033[1;35;40m<#> socket connected\u001b[0m')
        userInterface(sock)
    except Exception as e:
        print('\033[1;31;40m<-> Error on client side:\u001b[0m', str(e))


if __name__ == '__main__':
    main()