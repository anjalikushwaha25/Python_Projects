import json
from datetime import datetime

#expenses = []
#income= []

try:
    with open("data.json","r") as file:
        data = json.load(file)

    expenses = data.get("expenses",[])
    income = data.get("income",[])

except FileNotFoundError:
    expenses = [] 
    income= []

def save_data():
    data={
        "expenses": expenses,
        "income": income
    }

    with open("data.json","w")as file:
        json.dump(data,file,indent=4)

budget = 0
print("-------------------------------------------------------------")
print("Welcome to SmartExpense-Personal Expense Management System💰")
print("-------------------------------------------------------------")

while True:
    print("Hellooo, Here is the Menu👇")
    print("========MENU========")
    print("1. Add Expense➕")
    print("2. View all Expenses🫵")
    print("3. View Total Expense😲")
    print("4. Delete an Expense✂️")
    print("5. Update an Expense📝")
    print("6. Search an Expense🔎")
    print("7. Filter by Category⚓")
    print("8. Monthly Expense Summary")
    print("9. Set Monthly Budget")
    print("10. Category-wise Spending")
    print("11. Export Expenses to CSV")
    print("12. Add Income")
    print("13. View Total Income")
    print("14. View Savings")
    print("15. Expense Statistics")
    print("16. Exit👋")

    choice = int(input("Please Enter your choice🗃️:"))

#Add Expense

    if choice==1:
        
        category= input("Enter where money spent?(📕,🎒,🍔))")
        description = input("Describe about your expense🧾:")


        while True:
            try:
                amount = float(input("Enter the amount spent🤑:"))
                if amount<=0:
                    print("Amount must be greater than 0")
                else:
                    break

            except ValueError:
                print("Invalid amount! Please enter a number")

        while True:
            date = input("Enter the Date: (DD/MM/YYYY)📅:")

            try:
                datetime.strptime(date, "%d/%m/%Y")
                break
            except ValueError:
                print("Invalid date! Please enter in DD/MM/YYYY format📅:")


        expense = {
            "date": date,
            "category": category,
            "description": description,
            "amount": amount
        }

        expenses.append(expense)
        save_data()

        print("\n Expenses added successfully📝")

#View All Expense

    elif choice==2:
        if(len(expenses)==0):
            print("No Expenses added❌ ")
        else:
            print("Your Expenses are🧾:")
            count = 1
            for i in expenses:
                print(f"Expense {count}-> {i["date"]}, {i["category"]}, {i["description"]}, {i["amount"]}")
                count+=1

#View Total Expense

    elif choice==3:
        total = 0
        for i in expenses:
            total+=i["amount"]
        print("\n Total Expense is📝:", total)

#Delete an Expense

    elif choice==4:
        if(len(expenses)==0):
            print("No expense to delete📝")
        else:
            print("Your Expenses are🧾")
            count = 1
            for i in expenses:
                print(f"Expense {count}-> {i["date"]}, {i["category"]}, {i["description"]}, {i["amount"]}")
                count+=1

            number = int(input("Enter the expense number to delete🖊️:"))
            if number>=1 and number <=len(expenses):
                deleted_expense = expenses.pop(number - 1)

                save_data()

                print("Expense Deleted successfully❌")
                print("Deleted:", deleted_expense)

            else:
                print("Invalid expense number❌")

#Update an Expense

    elif choice==5:
        if(len(expenses)==0):
            print("No expenses to update🗃️")
        else:
            print("Your Expenses are🧾:")
            count = 1
            for i in expenses:
                print(f"Expense {count}-> {i["date"]}, {i["category"]}, {i["description"]}, {i["amount"]}")
                count+=1

            while True:
                try:
                    number = int(input("\nEnter the expense number to update:"))

                    if number<1 or number>len(expenses):
                        print("Invalid expense number!")
                    else:
                        break
                except ValueError:
                    print("Please enter a valid number")

            expense = expenses[number - 1]

            print("\n Enter new details")

            expense["category"] = input("Enter where money spent:")
            expense["description"] = input("Describe about your expense:")

            while True:
                try:
                    new_amount = float(input("Enter new amount"))
                    if new_amount<=0:
                        print("Amount must be greater than 0")
                    else:
                        expense["amount"]= new_amount
                        break
                except ValueError:
                    print("Invalid amount, Please neter a number")

            while True:
                new_date = input("Enter Date(DD/MM/YYYY):")
                try:
                    datetime.strptime(new_date,"%d/%m/%Y")
                    expense["date"] = new_date
                    break
                except ValueError:
                    print("Invalid date, Enter date(DD/MM/YYYY):")

            save_data()

            print("Expense updated successfully!!")
           

#Search an Expense

    elif choice==6:
        if(len(expenses)==0):
                print("No expenses to search🗃️")
        else:
            search = input("Enter description/category to search:").lower()

            found = False
            count = 1

            for i in expenses:
                if search in i["description"].lower() or search in i["category"].lower():
                    print(f"Expense {count}-> {i["date"]}, {i["category"]}, {i["description"]}, {i["amount"]}")
                    found = True
                    count+=1

                if found == False:
                    print("No matching expense found🙁")
                    
#Filter by Category

    elif choice==7:
        if(len(expenses)==0):
            print("No expenses🗃️")
        else:
            category = input("Enter category:").lower()

            found = False
            count = 1

            for i in expenses:
                if i["category"].lower() == category:
                    print(f"Expense {count}-> {i["date"]}, {i["category"]}, {i["description"]}, {i["amount"]}")
                    found = True
                    count +=1

            if found == False:
                print("No expenses found in this category🙁")

#Monthly Expense Summary

    elif choice==8:
        if(len(expenses)==0):
            print("No expenses available🗃️")
        else:
            month = input("Enter month(MM)📅:")
            year = input("Enter year(YYYY)📅")

            total = 0
            count = 0
            for i in expenses:
                date_parts = i["date"].split("/")

                expense_month = date_parts[1]
                expense_year = date_parts[2]

                if expense_month == month and expense_year == year:
                    total+=i["amount"]
                    count+=1

            print("\n Monthly Summary")
            print("---------------------")
            print("Month:", month)
            print("Year:", year)
            print("Number of expenses:",count)
            print("Total Expense", total)

#Set Monthly Budget

    elif choice==9:
        budget = float(input("Enter your monthly budget📝:"))

        total = 0
        for i in expenses:
            total+=i["amount"]

        print("Monthly Budget:", budget)
        print("Total Spent:", total)
        print("Remaining:", budget-total)

        if total>budget:
            print("⚠️Warning!\n You have exceeded your budget.")
        elif total>=budget*0.9:
            print("⚠️Warning! You have used more than 90% of your budget")
        else:
            print("You are within your budget.😁")

#Category-wise Spending

    elif choice==10:
        if(len(expenses)==0):
            print("No expenses available🗃️")
        else:
            categories = {}
            for i in expenses:
                category = i["category"]

                if category in categories:
                    categories[category]+=i["amount"]
                else:
                    categories[category] =i["amount"]

            print("\n Category-wise Spending")
            print("-----------------------------")

            for category, total in categories.items():
                print(f"{category}: {total}")

#Export Expenses to CSV

    elif choice==11:
        if(len(expenses)==0):
            print("No expenses available to export🗃️")
        else:
            import csv

            with open("expenses.csv", "w", newline="")as file:
                writer = csv.DictWriter(file, fieldnames=["date","category","description","amount"])
                writer.writeheader()
                writer.writerows(expenses)

            print("Expenses Exported successfully!!")
            print("File saves as expenses.csv")

#Add Income

    elif choice==12:
        amount = float(input("Enter your income amount:"))
        income.append(amount)

        save_data()

        print("Income added successfully!!")

#View Total Income

    elif choice==13:
        if len(income)==0:
            print("No income added!")
        else:
            total_income = 0

            for i in income:
                total_income +=i

            print("Total Income", total_income)

#View Savings

    elif choice==14:
        total_income=0
        total_expense=0

        for i in expenses:
            total_expense += i["amount"]

        for i in income:
            total_income +=i

        savings = total_income - total_expense

        print("\n---------Financial Summary-----------")
        print("Total Income: ",total_income)
        print("Total Expense: ", total_expense)
        print("Savings: ", savings)

        if savings <0:
            print(" ⚠️ You are spending more than your income!")
        else:
            print("Good! You are saving money.")

        if total_income>0:
            savings_rate = (savings/total_income)*100
            print("SAvings Rate:", round(savings_rate, 2),"%")
        else:
            savings_rate = 0

#Expense Statistics

    elif choice==15:
        if(len(expenses)==0):
            print("No expenses available🗃️")
        else:
            amounts = []

            for expense in expenses:
                amounts.append(expense["amount"])

            total = sum(amounts)
            highest = max(amounts)
            lowest = min(amounts)
            average = total/len(amounts)

            print("\n=========Expense Statistics=============")
            print(f"Total Expenses: {total:.2f}")
            print(f"Highest Expense: {highest:.2f}")
            print(f"Lowest Expense: {lowest:.2f}")
            print(f"Average Expense: {average:.2f}")
        print("=================================================")        

#Exit

    elif choice==16:
        print("Thankyou, Byeee!!👋")
        break
    else:
        print("Invalid Choice.")




    


