# Function to verify a single player's username and password
def authorise_player(username, password):
    # Remove any surrounding whitespace from the username
    username = username.strip()
    # Remove any surrounding whitespace from the password
    password = password.strip()

    # Open the authorised players file in read mode
    with open("Card Game Comp Sci/authorised_players.txt", "r") as file:
        # Read all lines from the file into a list
        lines = file.readlines()
        # Loop through each line in the file
        for line in lines:
            # Remove trailing newline/whitespace from the line
            line = line.strip()
            # Split the line into parts using comma as a delimiter
            parts = line.split(",")
            # Check if the stored username matches the entered username
            if parts[0] == username:
                # Check if the stored password matches the entered password
                if parts[1] == password:
                    # Credentials match: authentication successful
                    return True
                # Username matched but password did not: authentication fails
                return False
                
        
        # No matching username found in the file: authentication fails
        return False