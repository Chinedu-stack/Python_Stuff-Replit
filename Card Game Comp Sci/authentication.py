

def authentication():

    p1_username = input("Enter your username").strip()
    p1_password = input("Enter your password").strip()
    print()
    print()
    p2_username = input("Enter your username").strip()
    p2_password = input("Enter your password").strip()

    p1_check = authorise_player(p1_username, p1_password)
    p2_check = authorise_player(p2_username, p2_password)

    if p1_check and p2_check:
        return True
    return False

def authorise_player(username, password):
    username = username.strip()
    password = password.strip()

    with open("Card Game Comp Sci/authorised_players.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            parts = line.split(",")
            if parts[0] == username:
                if parts[1] == password:
                    return True
                return False
                
        
        return False

