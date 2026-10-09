# Import time and os modules for delays and clearing the screen
import time, os 
# Import authentication functions from the authentication module
from authentication import authorise_player 
# Import game-related classes from the classes module
from classes import Card, Deck, Player, Game 
 
# Flag to control whether the overall program should exit
exit_game = False 
# Main game loop: keeps running until the user chooses to exit
while not exit_game: 
 
    # Flag to track whether both players have been authorised
    authorised = False 
    # Authentication loop: repeats until both players are authorised or the user exits
    while not authorised and not exit_game: 
        # Prompt player 1 for their username, stripping surrounding whitespace
        p1_username = input("Player 1: Enter your username - ").strip() 
        # Prompt player 1 for their password, stripping surrounding whitespace
        p1_password = input("Player 1: Enter your password - ").strip() 
        # Print two blank lines for spacing
        print() 
        print() 
        # Prompt player 2 for their username, stripping surrounding whitespace
        p2_username = input("Player 2: Enter your username - ").strip() 
        # Prompt player 2 for their password, stripping surrounding whitespace
        p2_password = input("Player 2: Enter your password - ").strip() 
 
        # Verify player 1's credentials
        p1_check = authorise_player(p1_username, p1_password) 
        # Verify player 2's credentials
        p2_check = authorise_player(p2_username, p2_password) 
 
        # If both players are authorised
        if p1_check and p2_check: 
            # Prevent both players from being the same user
            if p1_username == p2_username: 
                print("Error. Cannot have both players as the same user. Please try again") 
                time.sleep(1) 
                # Clear the console screen
                os.system("cls") 
            else: 
                print("Success. Both users are authorised") 
                # Mark both players as authorised to exit the loop
                authorised = True 
                time.sleep(2) 
                os.system("cls") 
        else: 
            # One or both players failed authentication
            print("1 or more users not authorised. Please try again") 
            time.sleep(1) 
            os.system("cls") 
 
 
    # Game loop: runs while players are authorised and the user hasn't chosen to exit
    while authorised and not exit_game: 
        print("Welcome to the card game !!!") 
        print() 
        print() 
 
        # Create a new Game instance
        game = Game() 
        # Set up the game using the two authorised usernames
        game.set_up_game(p1_username, p2_username) 
        # Run the main gameplay
        game.play_game() 
 
        # Inner loop: ask the player what to do after a game ends
        while True: 
             
            # Prompt the user for their next action
            choice = input( 
                "Would you like to have a new game, log out, or exit?\n" 
                "1 = New game\n" 
                "2 = Log out\n" 
                "3 = Exit\n" 
                "Answer: " 
            ).strip().lower() 
             
            # Option 1: start a new game
            if choice == "1": 
                 
                print("New round loading in 2 seconds...") 
                time.sleep(2) 
                os.system("cls") 
                # Break to restart the game loop with a fresh Game instance
                break 
 
            # Option 2: log out and return to authentication
            elif choice == "2": 
 
                authorised = False 
                print("Logging out...") 
                time.sleep(1)  
                os.system("cls") 
                # Break to exit the game loop and return to authentication
                break 
 
            # Option 3: exit the program entirely
            elif choice == "3": 
                exit_game = True 
 
                break 
 
            # Any other input is invalid; ask again
            else: 
                print("Invalid Input. Try Again") 
 
    # Final message shown when the program ends
    print("Thanks for playing")