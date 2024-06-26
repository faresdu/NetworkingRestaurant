import socket
import pickle
import time
import sys
import getpass
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
        print('\033[1;31;40m<-> Invalid input! Please enter only letters.\u001b[0m')
        addedItem = input('->')
    
    sock.sendall(addedItem.encode())
    print('\033[1;33;40m<+> What is the price of the item?\u001b[0m\n')
    itemPrice = input('->')
    while not itemPrice.isdigit():
        print('\033[1;31;40m<-> Invalid input! Please enter only integers.\u001b[0m')
        itemPrice = input('->')
    sock.sendall(itemPrice.encode())

    print('\033[1;33;40m<+> What is the quantity of the item?\u001b[0m\n')
    itemQuantity = input('->')
    while not itemQuantity.isdigit():
        print('\033[1;31;40m<-> Invalid input! Please enter only integers.\u001b[0m')
        itemQuantity = input('->')
    sock.sendall(itemQuantity.encode())
    print('\033[1;37;40m<#> Item added successfuly!')

def deleteItem(sock):
    print('\033[1;33;40m<+> What item do you want to delete?\u001b[0m\n')
    deletedItem = input('->')
    sock.sendall(deletedItem.encode())
    respond = sock.recv(1024).decode()
    if respond=='1':
        print('\033[1;37;40m<#> item deleted successfully\u001b[0m')
    elif respond=='0':
        print('\033[1;31;40m<-> item not found, nothing has been deleted\u001b[0m')
        
def modifyItem(sock):
    print('\033[1;33;40m<+> What item do you want to modify?\u001b[0m\n')
    modifiedItem = input('->')
    while not modifiedItem.isalpha():
        print('\033[1;31;40m<-> Invalid input! Please enter only letters.\u001b[0m')
        modifiedItem = input('->')
    sock.sendall(modifiedItem.encode())

    print('\033[1;33;40m<+> What is the new price of the item?\u001b[0m\n')
    newPrice = input('->')
    while not newPrice.isdigit():
        print('\033[1;31;40m<-> Invalid input! Please enter only integers.\u001b[0m')
        newPrice = input('->')
    sock.sendall(newPrice.encode())

    print('\033[1;33;40m<+> What is the new quantity of the item?\u001b[0m\n')
    newQuantity = input('->')
    while not newQuantity.isdigit():
        print('\033[1;31;40m<-> Invalid input! Please enter only integers.\u001b[0m') 
        newQuantity = input('->')
    sock.sendall(newQuantity.encode())
    ackClient = sock.recv(1024).decode()
    if ackClient == '1':
        print('\033[1;37;40m<#> Item modified successfully!\u001b[0m\n')
    elif ackClient == '0':
        print('\033[1;31;40m<-> Something is wrong\u001b[0m')

def customerAuth(sock):
    try:
        sock.sendall(b'Customer')
        menuu=retrieveMenu(sock)

        loop = True
        meals = ''
        quantity = ''
        match=True
        while loop != False:
            match = False
            print("\033[1;33;40m<+> Enter your order\n\u001b[0m ", end=' ')
            cusOrder = input('-> ')
            for a in dict(menuu).keys():
                if a.lower() == cusOrder.lower():
                    match=True
            if match == False:
                print(f"\033[1;31;40m<-> There is no {cusOrder}\u001b[0m")
                continue

            print("\033[1;33;40m<+> Enter the quantity\n\u001b[0m ", end=' ')
            cusQuan = input('-> ')
            meals += cusOrder + ','
            quantity += cusQuan + ','
            print(meals)
            ans=''
            while ans != 'n' and ans != 'y':
                print("\033[1;33;40m<+> Did you finish(y/n)\n\u001b[0m", end=' ')
                ans = input('-> ')
            if ans=='y':
                loop=False


        sock.sendall(meals.encode())
        sock.sendall(quantity.encode())
        # trace

        msg = sock.recv(1024).decode()
        c=0
        while msg!='finish':
            msg = sock.recv(1024).decode()
            if msg=='0':

                diclinedOrder=sock.recv(1024).decode()
                diclinedOrderQuan = sock.recv(1024).decode()

                print(f"\033[1;31;40m<-> The Avaliable {diclinedOrder} is {diclinedOrderQuan} only!\u001b[0m")
                ans=''
                while ans!='n' and ans!='y':
                    print(f"\033[1;33;40m<+> Do you want to order {diclinedOrder}?(y/n)\n\u001b[0m ", end="")
                    ans = input('-> ')

                if ans =="y":
                    print(f"\033[1;33;40m<+> How many {diclinedOrder} do you need? (Amount has to be less than {diclinedOrderQuan})\n\u001b[0m ", end="")
                    anq = input('-> ')
                    while anq>=diclinedOrderQuan:
                        print(f"\033[1;33;40m<+> How many Quantity (Enter less than {diclinedOrderQuan})\n\u001b[0m", end="")
                        anq = input('-> ')

                    sock.sendall(b"y")
                    sock.sendall(anq.encode())
                elif ans=='n':
                    sock.sendall(b'n')

        totalBill = sock.recv(1024).decode()

        if int(totalBill)==0:
            print("\033[1;34;40m<#> Thank you\u001b[0m")
            sock.sendall(b'0')
        else:
            print(f"\033[1;37;40m<#> Your Bill is {totalBill} SAR\u001b[0m")
            confirm=''
            while confirm!='n' and confirm!='y':
                print("\033[1;33;40m<+> Do you confirm your order(y/n)\n\u001b[0m", end=' ')
                confirm = input('-> ')
            if confirm == 'y':
                print("\033[1;33;40m<+> Enter your address\n\u001b[0m ", end=' ')
                addr = input('-> ')
                sock.sendall(b'1')
                sock.sendall(addr.encode())
                ACK = sock.recv(1024).decode()
                if ACK == '1':
                    print(f"\033[1;34;40m<#> Your order has been accepted by the restaurant and will be delivered to {addr}\u001b[0m")
                    toolbar_width = 40
                    print('<#> Leaving to main screen')
                    sys.stdout.write("[%s]" % (" " * toolbar_width))
                    sys.stdout.flush()
                    sys.stdout.write("\b" * (toolbar_width+1)) 
                    
                    for i in range(toolbar_width):
                        time.sleep(0.1) 
                        sys.stdout.write("■")
                        sys.stdout.flush()

                    sys.stdout.write("]\n") 
            elif confirm == 'n':
                sock.sendall(b'0')

    except Exception as e:
        print(f"\033[1;31;40m<-> Something went wrong! {str(e)}\u001b[0m")
        

def retrieveMenu(sock):
    data = sock.recv(1024)
    data = pickle.loads(data)


    print('\033[1;36;40m =============================== \u001b[0m')
    print('\033[1;36;40m =\u001b[0m meals             price(SAR)\033[1;36;40m =\u001b[0m')
    for i,k in data.items():
        print('\033[1;36;40m =\u001b[0m',i,end='')
        for l in range(0,18-len(str(i))):
            print(end=' ')
        print(k['price'],end='')
        for l in range(0, 10 - len(str(k['price']))):
            print(end=' ')

        print("\033[1;36;40m = \u001b[0m")
    print('\033[1;36;40m =============================== \u001b[0m')
    return data

def ownerAuth(sock):
    try:
            print('\033[1;33;40m<+> Enter your username:\u001b[0m')
            username = input('->')
            sock.sendall(username.encode())
            print('\033[1;33;40m<+> Enter your password:\u001b[0m')
            password = getpass.getpass(prompt='(Password is hidden)-> ')
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