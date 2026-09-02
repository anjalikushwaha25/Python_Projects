import time

USERNAME = "Anjali"
PASSWORD = "1234"

print("-----------Cafe Management Login Portal------------")
time.sleep(2)

name = input("Enter username: ")
pswd = input("Enter password: ")

if name != USERNAME or pswd != PASSWORD:
    print("Access Denied!! Invalid Credentials")
    exit()
else:
    print(f"Login Successful!! Welcome {name}")
    print("-"*40)
time.sleep(3)

print("************************")
print("Welcome to the Cafe🏨")
print("************************")

time.sleep(2)

menu= { "pizza" : 3,
        "maggie" : 6,
        "pasta" : 23,
        "lemon" : 45,
        "water":76}
cart = []
total = 0

print("------------MENU------------")
for key, value in menu.items():
    print(f"{key:10}: ${value:.2f}")
print("--------------------------")

while True:
    food = input("Select an item(q to quit):")
    if food.lower() == 'q':
        break
    elif menu.get(food) is not None:
        try:
            qty = int(input("Enter the quantity: "))
            if qty <= 0:
                print("Quantity must be atleast 1!!")
                continue

            cart.append((food,qty))
        except ValueError:
            print("Plz Enter valid number!!")
    else:
        print("Item not found!!")
    
print(cart)
print("Please Wait for your Bill!!")
time.sleep(3)
print("-----------YOUR BILL----------")
for food,qty in cart:
    price = menu[food]* qty
    total += price
    print(f"{food} * {qty} = {price:2f}")

print()
print(f"Total is: ${total:.2f}")
print("Thank you for ordering visit again!!")
print("-"* 40)

print("--------Payment Options--------")

print("1. Cash")
print("2. UPI")
print("3. Card")

choice = input("Select your payment mode(1/2/3): ")
if choice == '1':
    print("Payment Received in Cash. Thankyou!")
elif choice == '2':
    print("Payment Received via UPI. Thankyou!")
elif choice == '3':
    print("Payment Received via Card. Thankyou!")
else:
    print("Invalid Option Selected!!")

time.sleep(2)

print("-"* 40)
print("We'd love your feedback💌!!")

name = input("Enter your name: ")
rating = input("Rate us(1-5)⭐: ")
comment = input("Any comments💬? ")

print(f"Thank You, for your feedback {name}😊")
print("Your rating⭐: ", rating)
print("Your comment💬: ", comment)
print("*"*40)
print("We hope to serve you again🍴!!")
print("*"*40)


