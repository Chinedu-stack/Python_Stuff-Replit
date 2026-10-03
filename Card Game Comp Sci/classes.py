# Import random module for shuffling the deck
import random
# Import time and os modules for delays and clearing the screen
import time, os

# Class representing a single playing card with a colour and a number
class Card:
    # Initialise a card with a colour and a number
    def __init__(self, colour, number):
        self.colour = colour
        self.number = number
        
    # Return a readable string representation of the card
    def __str__(self):
        return f"The card has the colour {self.colour} and is number of {self.number}"

# Class representing a deck of cards
class Deck:
    # Initialise an empty deck and define the available colours
    def __init__(self):
        self.cards = []
        self.colours = ["red", "black", "yellow"]

    # Populate the deck with cards: numbers 1-10 for each colour
    def create_deck(self):
        for i in range(1,11):
            for colour in self.colours:
                card = Card(colour, i)
                self.cards.append(card)

    # Shuffle the deck to randomise the card order
    def shuffle(self):
        '''
        it changes the order of the cards in the deck randomly
        '''
        random.shuffle(self.cards)

    # Draw the top card from the deck and remove it from the deck
    def draw_card(self):
        drawn_card = self.cards[0]
        self.cards.remove(drawn_card)
        return drawn_card

    # Return the number of cards left in the deck
    def cards_remaining(self):
        return len(self.cards)

    # Check whether the deck has no cards left
    def is_empty(self):
        if len(self.cards) == 0:
            return True
        return False

# Class representing a player in the game
class Player:
    # Initialise a player with a name, empty won-cards list, and no current card
    def __init__(self, name):
        self.name = name
        self.won_cards = []
        self.current_card = None

    # Return how many cards the player has won
    def get_card_count(self):
        return len(self.won_cards)
    
    # Reset the player's current card back to None
    def reset_current_card(self):
        self.current_card = None

    # Return a readable string representation of the player
    def __str__(self):
        return f"Player name is {self.name} they have won {len(self.won_cards)} cards."
    
# Class representing the overall game logic
class Game:
    # Initialise the game with no players, no deck, and colour rules
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.deck = None
        self.round_winner = None
        # Rules defining which colour beats which
        self.colour_rules = {
            "red": "black",
            "yellow": "red",
            "black": "yellow"
        }
        self.game_round = 1
        self.overall_winner = None

    # Set up the game by creating players, building the deck, and shuffling it
    def set_up_game(self, player1_name, player2_name):
        self.player1 = Player(player1_name)
        self.player2 = Player(player2_name)

        self.deck = Deck()
        self.deck.create_deck()
        self.deck.shuffle()

    # Compare the two players' current cards and return the round winner
    def card_comparison(self):
        # If both cards share the same colour, higher number wins
        if self.player1.current_card.colour == self.player2.current_card.colour:
            if self.player1.current_card.number > self.player2.current_card.number:
                return self.player1
            elif self.player1.current_card.number < self.player2.current_card.number:
                return self.player2
            else:
                # Equal colour and number means a draw
                return None
        else:
            # Otherwise use the colour rules to determine the winner
            p1_beats = self.colour_rules[self.player1.current_card.colour]
            if self.player2.current_card.colour == p1_beats:
                return self.player1
            else:
                return self.player2
                
    # Reset both players' current cards
    def reset_current_cards(self):
        self.player1.reset_current_card()
        self.player2.reset_current_card()

    # Main gameplay loop: play rounds until the deck has fewer than 2 cards
    def play_game(self):
        while self.deck.cards_remaining() >= 2:

            print("------------------------------")
            print(f"Round {self.game_round}")
            print("------------------------------")

            ### Player 1 drawing card
            card1 = self.deck.draw_card()
            self.player1.current_card = card1
            print(f"Player 1 card:  {self.player1.current_card}")

            ### Player 2 drawing card
            card2 = self.deck.draw_card()
            self.player2.current_card = card2
            print(f"Player 2 card:  {self.player2.current_card}")

            ### Card Comparison
            winner = self.card_comparison()
            # If there is a winner, award them both cards
            if winner != None:
                winner.won_cards.extend([self.player1.current_card, self.player2.current_card])
                self.round_winner = winner
                print(f"The winner of this round is {winner.name}")

            # Otherwise, it was a draw
            else:
                print("It is a draw.")

            ### clear current card of both players
            self.reset_current_cards()
            self.game_round += 1



        print("------------------------------")
        print(f"Round Over")
        print("------------------------------")

        # Determine the overall winner after all rounds are played
        self.overall_winner = self.determine_overall_winner()

        # If there is a winner, display, save, and show leaderboard
        if self.overall_winner:
            print("------------------------------")
            print(f"The winner is {self.overall_winner.name} with {len(self.overall_winner.won_cards)} cards won")
            print("------------------------------")

            self.save_result()
            print()
            print()
            self.show_leaderboard()


        # Otherwise, announce a draw
        else:
            print("------------------------------")
            print(f"It was a draw with both players having won {len(self.player1.won_cards)} cards")
            print("------------------------------")

    # Determine which player won overall based on number of cards won
    def determine_overall_winner(self):
        if len(self.player1.won_cards) > len(self.player2.won_cards):
            return self.player1
        elif len(self.player1.won_cards) == len(self.player2.won_cards):
            # Equal cards means a draw
            return None
        else:
            return self.player2

    # Append the overall winner's result to the results file
    def save_result(self):
        if self.overall_winner:
            with open("Card Game Comp Sci/results.txt", "a") as file:
                file.write(f"{self.overall_winner.name},{len(self.overall_winner.won_cards)} \n")

    # Read, sort, and display the top 5 players from the results file
    def show_leaderboard(self):
        players_list = []
        with open("Card Game Comp Sci/results.txt", "r") as file:
            lines = file.readlines()
            # Parse each line into [name, score] format
            for line in lines:
                player_data = line.split(",")
                player_data[1] = int(player_data[1])
                players_list.append(player_data)

            # Sort players by score in descending order
            players_list.sort(key=lambda player: player[1], reverse=True)

            print("Current Leaderboard: Top 5 players \n\n\n ")
            # Display the top 5 players if any exist
            if players_list:
                for player in players_list[:5]:
                    print(f"Name: {player[0]}   Amount of cards won: {player[1]}")
            # Otherwise show a message indicating the leaderboard is empty
            else:
                print("No players in the leaderboard")