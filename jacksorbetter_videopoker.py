from misc.hand_evaluator import HandEvaluator
from misc.deck import Deck

# Define ANSI escape codes for colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"

class JacksOrBetter:
    def __init__(self):
        self.net_profit = 0
        self.deck = Deck()
        self.evaluator = HandEvaluator()
        self.current_bet = 0

    def play(self):
        print(f"{CYAN}Welcome to Jacks or Better Video Poker!{RESET}")
        while True:
            if self.current_bet == 0:
                self.current_bet = self.get_bet()

            print(f"\n{BLUE}Current Net Profit/Loss: {self.net_profit} credits{RESET}")
            self.deck = Deck()
            hand = self.deck.deal(5)
            print(f"{MAGENTA}Your hand:{RESET}", ', '.join(str(card) for card in hand))

            held_indices = self.get_held_cards()
            self.final_hand = self.redraw_cards(hand, held_indices)
            print(f"{MAGENTA}Your final hand:{RESET}", ', '.join(str(card) for card in self.final_hand))

            hand_rank = self.evaluator.best_hand(self.final_hand, [])
            payout = self.calculate_payout(hand_rank[0])

            self.net_profit += payout - self.current_bet

            hand_type = self.evaluator.hand_type(hand_rank[0])
            if payout > 0:
                print(f"{GREEN}Hand Type: {hand_type}{RESET}")
                print(f"{GREEN}Payout: {payout} credits{RESET}")
            else:
                print(f"{RED}Hand Type: {hand_type}{RESET}")
                print(f"{RED}No Payout{RESET}")
            
            print(f"{BLUE}New Net Profit/Loss: {self.net_profit} credits{RESET}")

            next_action = self.get_next_action()
            if next_action == 'stop':
                print(f"{BLUE}Final Net Profit/Loss: {self.net_profit} credits{RESET}")
                break
            elif next_action == 'change':
                self.current_bet = 0

    def get_bet(self):
        while True:
            try:
                bet = int(input(f"{CYAN}Enter your bet (any amount of credits): {RESET}"))
                if bet > 0:
                    return bet
                else:
                    print(f"{RED}Bet amount must be greater than zero.{RESET}")
            except ValueError:
                print(f"{RED}Please enter a valid number.{RESET}")

    def get_held_cards(self):
        held_cards = input(f"{YELLOW}Enter the positions (1-5) of the cards you want to hold, separated by spaces (e.g., '1 3 5'): {RESET}")
        return [int(pos) - 1 for pos in held_cards.split() if pos.isdigit() and 1 <= int(pos) <= 5]

    def redraw_cards(self, hand, held_indices):
        new_hand = [hand[i] for i in held_indices]
        new_hand += self.deck.deal(5 - len(held_indices))
        return new_hand

    def calculate_payout(self, hand_rank):
        payout_table = {
            0: 0,   # High Card
            1: 1 * self.current_bet + self.current_bet,   # One Pair (must be Jacks or Better)
            2: 2 * self.current_bet + self.current_bet,   # Two Pair
            3: 3 * self.current_bet + self.current_bet,   # Three of a Kind
            4: 4 * self.current_bet + self.current_bet,   # Straight
            5: 5 * self.current_bet + self.current_bet,   # Flush
            6: 8 * self.current_bet + self.current_bet,   # Full House
            7: 25 * self.current_bet + self.current_bet,  # Four of a Kind
            8: 50 * self.current_bet + self.current_bet,  # Straight Flush
            9: 250 * self.current_bet + self.current_bet  # Royal Flush
        }

        if hand_rank == 1:
            pair_cards = self.evaluator.best_hand(self.final_hand, [])[1]
            pair_rank = self.evaluator.card_rank(pair_cards[0])
            if pair_rank < 11:  # If less than Jacks
                return 0

        return payout_table.get(hand_rank, 0)

    def get_next_action(self):
        while True:
            action = input(f"{CYAN}Do you want to stop playing (s), replay again with the same bet (r), or change bet size (c)?\n Enter s, r, or c: {RESET}").lower()
            if action == 's':
                return 'stop'
            elif action == 'r':
                return 'play_again'
            elif action == 'c':
                return 'change'
            else:
                print(f"{RED}Invalid input. Please enter s, r, or c.{RESET}")

if __name__ == "__main__":
    game = JacksOrBetter()
    game.play()
