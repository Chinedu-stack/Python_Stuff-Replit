import time, os
from authentication import authentication, authorise_player
from classes import Card, Deck, Player, Game


authorised = False
while not authorised:
    p1_username = input("Enter your username").strip()
    p1_password = input("Enter your password").strip()
    print()
    print()
    p2_username = input("Enter your username").strip()
    p2_password = input("Enter your password").strip()

    p1_check = authorise_player(p1_username, p1_password)
    p2_check = authorise_player(p2_username, p2_password)

    if p1_check and p2_check:
        print("Success. Both users are authorised")
        time.sleep(2)
        os.system("cls")