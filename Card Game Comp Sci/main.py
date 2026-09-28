import time, os
from authentication import authentication, authorise_player
from classes import Card, Deck, Player, Game

exit_game = False
while not exit_game:

    authorised = False
    while not authorised and not exit_game:
        p1_username = input("Player 1: Enter your username - ").strip()
        p1_password = input("Player 1: Enter your password - ").strip()
        print()
        print()
        p2_username = input("Player 2: Enter your username - ").strip()
        p2_password = input("Player 2: Enter your password - ").strip()

        p1_check = authorise_player(p1_username, p1_password)
        p2_check = authorise_player(p2_username, p2_password)

        if p1_check and p2_check:
            if p1_username == p2_username:
                print("Error. Cannot have both players as the same user. Please try again")
                time.sleep(1)
                os.system("cls")
            else:
                print("Success. Both users are authorised")
                authorised = True
                time.sleep(2)
                os.system("cls")
        else:
            print("1 or more users not authorised. Please try again")
            time.sleep(1)
            os.system("cls")


    while authorised and not exit_game:
        print("Welcome to the card game !!!")
        print()
        print()

        game = Game()
        game.set_up_game(p1_username, p2_username)
        game.play_game()

        while True:
            
            choice = input( "Would you like to have a new game, log out, or exit?\n" "1 = New game\n" "2 = Log out\n" "3 = Exit\n" "Answer: " ).strip().lower()
            
            if choice == "1":
                
                print("New round loading in 2 seconds...")
                time.sleep(2)
                os.system("cls")
                break

            elif choice == "2":

                authorised = False
                print("Logging out...")
                time.sleep(1) 
                os.system("cls")
                break

            elif choice == "3":
                exit_game = True

                break

            else:
                print("Invalid Input. Try Again")

    print("Thanks for playing")





