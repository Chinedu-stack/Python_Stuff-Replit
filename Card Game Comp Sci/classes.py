import random
import time, os

class Card:
    def __init__(self, colour, number):
        self.colour = colour
        self.number = number
        
    def __str__(self):
        return f"The card has the colour {self.colour} and is number of {self.number}"

class Deck:
    def __init__(self):
        self.cards = []
        self.colours = ["red", "black", "yellow"]

    def create_deck(self):
        for i in range(1,11):
            for colour in self.colours:
                card = Card(colour, i)
                self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        drawn_card = self.cards[0]
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

    def get_card_count(self):
        return len(self.won_cards)
    
    def reset_current_card(self):
        self.current_card = None

    def __str__(self):
        return f"Player name is {self.name} they have won {len(self.won_cards)} cards."
    
class Game:
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.deck = None
        self.round_winner = None
        self.colour_rules = {
            "red": "black",
            "yellow": "red",
            "black": "yellow"
        }
        self.game_round = 1
        self.overall_winner = None

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
            p1_beats = self.colour_rules[self.player1.current_card.colour]
            if self.player2.current_card.colour == p1_beats:
                return self.player1
            else:
                return self.player2
                
    def reset_current_cards(self):
        self.player1.reset_current_card()
        self.player2.reset_current_card()

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
            if winner != None:
                winner.won_cards.extend([self.player1.current_card, self.player2.current_card])
                self.round_winner = winner
                print(f"The winner of this round is {winner.name}")

            else:
                print("It is a draw.")

            ### clear current card of both players
            self.reset_current_cards()
            self.game_round += 1



        print("------------------------------")
        print(f"Round Over")
        print("------------------------------")

        self.overall_winner = self.determine_overall_winner()

        if self.overall_winner:
            print("------------------------------")
            print(f"The winner is {self.overall_winner.name} with {len(self.overall_winner.won_cards)} cards won")
            print("------------------------------")

            self.save_result()
            print()
            print()
            self.show_leaderboard()


        else:
            print("------------------------------")
            print(f"It was a draw with both players having won {len(self.player1.won_cards)} cards")
            print("------------------------------")

    def determine_overall_winner(self):
        if len(self.player1.won_cards) > len(self.player2.won_cards):
            return self.player1
        elif len(self.player1.won_cards) == len(self.player2.won_cards):
            return None
        else:
            return self.player2

    def save_result(self):
        if self.overall_winner:
            with open("Card Game Comp Sci/results.txt", "a") as file:
                file.write(f"{self.overall_winner.name},{len(self.overall_winner.won_cards)} \n")

    def show_leaderboard(self):
        players_list = []
        with open("Card Game Comp Sci/results.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                player_data = line.split(",")
                player_data[1] = int(player_data[1])
                players_list.append(player_data)

            players_list.sort(key=lambda player: player[1], reverse=True)

            print("Current Leaderboard: Top 5 players \n\n\n ")
            if players_list:
                for player in players_list[:5]:
                    print(f"Name: {player[0]}   Amount of cards won: {player[1]}")
            else:
                print("No players in the leaderboard")
            











