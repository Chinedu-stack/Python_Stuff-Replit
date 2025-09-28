import time, os 
 
list = []
def pl():
 for index in range(len(list)):
        print(f"\033[94m{index+1}: {list[index]}\033[0m")


while True:
    print("Wonderful List of Chinedu😍👌❤️📃💕😘🤣😂😊")
    print()
    print()
    word = input("What would you like to add to you list:\n")
    if word not in list:
        list.append(word)
        print()
        print("Here is your updated list: ")
        print()
        pl()
        time.sleep(2)
        os.system("cls")
    else:
        print()
        print(f"Sorry {word} is already in your list")
        print("Please try again 😒")
        time.sleep(2)
        os.system("clear")


