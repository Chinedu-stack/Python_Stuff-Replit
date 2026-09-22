import random

class Card:
    def __init__(self, colour, number):
        self.colour = colour
        self.number = number
        
    def __str__(self):
        return f"The card has the colour {self.colour} and is number of {self.number}"

class Deck:
    def __init__(self, current_index=None):
        self.cards = []
        self.current_index = current_index
        self.colours = ["red", "black", "yellow"]

    def create_deck(self):
        for i in range(1,11):
            for colour in self.colours:
                card = Card(colour, i)
                self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self, current_index):
        drawn_card = self.cards[current_index]
        self.cards.remove(drawn_card)
        return drawn_card

    def cards_remaining(self):
        return len(self.cards)

    def is_empty(self):
        if len(self.cards) == 0:
            return True
        return False

class Player:
    def __init__(self, name):
        self.name = name
        self.won_cards = []
        self.current_card = None

    def add_cards(self, card):
        self.won_cards.append(card)

    def get_card_count(self):
        return len(self.won_cards)
    
    def reset_cards(self):
        self.current_card = None

    def __str__(self):
        return f"Player name is {self.name} they have won {len(self.won_cards)} cards."
    
class Game:
    def __init__(self,  leaderboard):
        self.player1 = None
        self.player2 = None
        self.deck = None
        self.winner = None
        self.leaderboard = leaderboard
        self.current_index = 1
        self.colour_rules = {
            "red": "black",
            "yellow": "red",
            "black": "yellow"
        }

    def set_up_game(self, player1_name, player2_name):
        self.player1 = Player(player1_name)
        self.player2 = Player(player2_name)

        self.deck = Deck()
        self.deck.create_deck()
        self.deck.shuffle()

    def card_comparison(self):
        if self.player1.current_card.colour == self.player2.current_card.colour:
            if self.player1.current_card.number > self.player2.current_card.number:
                return self.player1
            elif self.player1.current_card.number < self.player2.current_card.number:
                return self.player2
            else:
                return None
        else:
            losing_colour = self.colour_rules[self.player1.current_card.colour]
            if self.player2.current_card.colour == losing_colour:
                return self.player1
            else:
                return self.player2
                
    def reset_current_cards(self):
        self.player1.reset_cards()
        self.player2.reset_cards()

    def play_round(self):
        while self.deck.is_empty == False:
            ### Player 1 drawing card
            card = self.deck.draw_card(self.current_index)
            self.current_index += 1
            self.player1.current_card = card

            ### Player 2 drawing card
            card2 = self.deck.draw_card(self.current_index)
            self.current_index += 1
            self.player2.current_card = card

            ### Card Comparison
            winner = self.card_comparison()
            if winner != None:
                winner.won_cards.extend([self.player1.current_card, self.player2.current_card])
                self.winner = winner
                print(f"The winner of this round is {winner.name}")
            else:
                print("It is a draw.")

            ### clear current card of both players
            self.reset_current_cards()

    def save_result(self):
        if self.winner:
            with open("results.txt", "a") as file:
                file.write(f"{self.winner.name},{len(self.winner.won_cards)} \n")

    def show_leaderboard(self):
        players_list = []
        with open("results.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                player_data = line.split(",")
                player_data[1] = int(player_data[1])
                players_list.append(player_data)

            players_list.sort(key=lambda player: player[1], reverse=True)

            print("Current Leaderboard: \n\n\n ")
            for player in players_list[:5]:
                print(f"Name: {player[0]}   Amount of cards won: {player[1]}")
            











