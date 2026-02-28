import random


num = random.randint(1, 100)
attempts = 0
answer = ""

while answer != num:
    answer = int(input("Guess number: "))
    if num == answer:
        print("correct")
   
    elif  1 < answer >  100:
        attempts += 1
        print("Invalid number. Try again. Attempts: {attempts}")
        
    elif answer > num:
        attempts += 1
        print(f"Try again. Number is too high. Attempts: {attempts}")
    else:
        attempts += 1
        print(f"Try again. Number is too low. Attempts: {attempts}")
        

