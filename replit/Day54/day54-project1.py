import csv


####🔹 Mini Project 1 (Easy): Shopping List Saver

###Ask the user for 3 shopping items.

###Save them into a CSV file with columns: item, quantity.

###Read the file back and print the list.








item1 = input("Item: ")
quantity1 = input("Quantity: ")
item2 = input("Item: ")
quantity2 = input("Quantity: ")
item3 = input("Item: ")
quantity3 = input("Quantity: ")
try:
    with open("food.csv", "w", newline="") as file:
        w = csv.writer(file)
        w.writerow(["food", "quantity"])
        w.writerow([item1, quantity1])
        w.writerow([item2, quantity2])
        w.writerow([item3, quantity3])


    with open("food.csv", "r") as file:
        r = csv.reader(file)
        for row in r:
            print(f"{row[0]}: {row[1]}")

except:
    print("Sorry this doesn't work")