import time
from misc.deck import Deck
import misc.ansicolors as colors

class Baccarat:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = []
        self.banker_hand = []
        self.bets = {"Player": 0, "Banker": 0, "Tie": 0, "Player Pair": 0, "Banker Pair": 0, "Lucky 6": 0}
        self.bank_commission = 0.05  # 5% commission on banker bets
        self.total_net_profit = 0
        self.round_net_profit = 0

    def card_value(self, card):
        if card.rank in ['10', 'J', 'Q', 'K']:  # 10, J, Q, K have a value of 0
            return 0
        elif card.rank == 'A':  # Ace has a value of 1
            return 1
        else:
            return int(card.rank)

    def calculate_hand_total(self, hand):
        total = sum(self.card_value(card) for card in hand)
        return total % 10

    def initial_deal(self):
        print(f"{colors.CYAN}Dealing cards...{colors.RESET}")
        time.sleep(1.5)
        self.player_hand = self.deck.deal(2)
        self.banker_hand = self.deck.deal(2)
        print(f"{colors.YELLOW}Player Hand: {self.player_hand[0]}, {self.player_hand[1]} (Total: {self.calculate_hand_total(self.player_hand)}){colors.RESET}")
        print(f"{colors.YELLOW}Banker Hand: {self.banker_hand[0]}, {self.banker_hand[1]} (Total: {self.calculate_hand_total(self.banker_hand)}){colors.RESET}")
        time.sleep(1)

    def check_natural(self, player_total, banker_total):
        if player_total >= 8 or banker_total >= 8:
            print(f"{colors.GREEN}Natural win!{colors.RESET}")
            return True
        return False

    def player_third_card_rule(self, player_total):
        return player_total <= 5

    def banker_third_card_rule(self, banker_total, player_third_card):
        if banker_total <= 2:
            return True
        elif banker_total == 3 and player_third_card != 8:
            return True
        elif banker_total == 4 and player_third_card in [2, 3, 4, 5, 6, 7]:
            return True
        elif banker_total == 5 and player_third_card in [4, 5, 6, 7]:
            return True
        elif banker_total == 6 and player_third_card in [6, 7]:
            return True
        return False

    def play_hand(self):
        self.initial_deal()
        player_total = self.calculate_hand_total(self.player_hand)
        banker_total = self.calculate_hand_total(self.banker_hand)

        if self.check_natural(player_total, banker_total):
            time.sleep(1)
            return self.decide_winner()

        if self.player_third_card_rule(player_total):
            print(f"{colors.CYAN}Player draws a third card...{colors.RESET}")
            time.sleep(1.5)
            player_third_card = self.deck.deal(1)[0]
            self.player_hand.append(player_third_card)
            player_total = self.calculate_hand_total(self.player_hand)
            print(f"{colors.YELLOW}Player's Hand: {self.player_hand} (Total: {player_total}){colors.RESET}")
        else:
            player_third_card = None

        if player_third_card is not None:
            if self.banker_third_card_rule(banker_total, self.card_value(player_third_card)):
                print(f"{colors.CYAN}Banker draws a third card...{colors.RESET}")
                time.sleep(1.5)
                banker_third_card = self.deck.deal(1)[0]
                self.banker_hand.append(banker_third_card)
                banker_total = self.calculate_hand_total(self.banker_hand)
                print(f"{colors.YELLOW}Banker's Hand: {self.banker_hand} (Total: {banker_total}){colors.RESET}")

        time.sleep(1)
        return self.decide_winner()

    def decide_winner(self):
        player_total = self.calculate_hand_total(self.player_hand)
        banker_total = self.calculate_hand_total(self.banker_hand)

        if player_total > banker_total:
            print(f"{colors.GREEN}Player wins!{colors.RESET}")
            if self.bets["Player"] > 0:
                self.round_net_profit += self.bets["Player"] * 2
                print(f"{colors.GREEN}You win {self.bets['Player']}!{colors.RESET}")
        elif banker_total > player_total:
            print(f"{colors.GREEN}Banker wins!{colors.RESET}")
            if self.bets["Banker"] > 0:
                self.round_net_profit += self.bets["Banker"] * 2
                win_amount = self.bets["Banker"] * (1 - self.bank_commission)
                print(f"{colors.GREEN}You win {win_amount} after commission!{colors.RESET}")
        else:
            print(f"{colors.YELLOW}It's a tie!{colors.RESET}")
            if self.bets["Tie"] > 0:
                self.round_net_profit += self.bets["Tie"] * 9
                print(f"{colors.GREEN}You win {self.bets['Tie'] * 9}!{colors.RESET}")

        time.sleep(1)
        self.check_pairs()
        time.sleep(1)
        self.check_lucky_6()

        total_bet = sum(amount for amount in self.bets.values())
        self.round_net_profit -= total_bet

        print(f"{colors.MAGENTA}Net profit this round: {self.round_net_profit}{colors.RESET}")
        self.total_net_profit += self.round_net_profit

        print(f"{colors.MAGENTA}Total net profit so far: {self.total_net_profit}{colors.RESET}")
        return self.round_net_profit

    def check_pairs(self):
        if self.bets["Player Pair"] > 0:
            if self.player_hand[0].rank == self.player_hand[1].rank:
                net_profit += self.bets["Player Pair"] * 12
                print(f"{colors.GREEN}Player hand is a pair! You win {self.bets['Player Pair'] * 12}!{colors.RESET}")
            else:
                print(f"{colors.RED}No Player Pair in this round.{colors.RESET}")
        
        if self.bets["Banker Pair"] > 0:
            if self.banker_hand[0].rank == self.banker_hand[1].rank:
                net_profit += self.bets["Banker Pair"] * 12
                print(f"{colors.GREEN}Banker hand is a pair! You win {self.bets['Banker Pair'] * 12}!{colors.RESET}")
            else:
                print(f"{colors.RED}No Banker Pair in this round.{colors.RESET}")

    def check_lucky_6(self):
        if self.bets["Lucky 6"] > 0:
            banker_total = self.calculate_hand_total(self.banker_hand)
            if banker_total == 6:
                if len(self.banker_hand) == 2:
                    net_profit += self.bets["Lucky 6"] * 13
                    print(f"{colors.GREEN}Banker wins with two-card 6! You win {self.bets['Lucky 6'] * 13}!{colors.RESET}")
                elif len(self.banker_hand) == 3:
                    net_profit += self.bets["Lucky 6"] * 21
                    print(f"{colors.GREEN}Banker wins with three-card 6! You win {self.bets['Lucky 6'] * 21}!{colors.RESET}")
            else:
                print(f"{colors.RED}Lucky 6 didn't win this round.{colors.RESET}")

    def place_bets(self):
        print(f"{colors.CYAN}Enter what you want to bet on {colors.YELLOW}(Player (p), Banker (b), Tie (t), Player Pair (pp), Banker Pair (bp), Lucky 6 (6)){colors.CYAN} followed by how much you want to bet (e.g., p 10). Type 'f' when finished.{colors.RESET}")
        while True:
            bet_input = input(f"{colors.YELLOW}Place your bet or enter 'f': {colors.RESET}").lower()
            if bet_input == "f":
                break
            try:
                bet_type, amount = bet_input.split()
                amount = int(amount)
                if bet_type in ["p", "b", "t", "pp", "bp", "6"]:
                    if bet_type == "p":
                        bet_type = "Player"
                    elif bet_type == "b":
                        bet_type = "Banker"
                    elif bet_type == "t":
                        bet_type = "Tie"
                    elif bet_type == "pp":
                        bet_type = "Player Pair"
                    elif bet_type == "bp":
                        bet_type = "Banker Pair"
                    elif bet_type == "6":
                        bet_type = "Lucky 6"
                    self.bets[f"{bet_type}"] += amount
                    print(f"{colors.GREEN}Bet placed: {bet_type}, ${amount} (Total: ${self.bets[f"{bet_type}"]}).{colors.RESET}")
                else:
                    print(f"{colors.RED}Invalid bet type. Please try again.{colors.RESET}")
            except ValueError:
                print(f"{colors.RED}Invalid format. Please enter the bet type followed by the amount (e.g., player 10).{colors.RESET}")

        print(f"{colors.MAGENTA}Bets closed.\nYour final bets: {', '.join([f'{colors.YELLOW}{bet}: {amount}' for bet, amount in self.bets.items() if amount > 0])}{colors.RESET}")

    def start_game(self):
        print(f"{colors.CYAN}Welcome to Baccarat!{colors.RESET}")
        time.sleep(1)
        while True:
            self.bets = {"Player": 0, "Banker": 0, "Tie": 0, "Player Pair": 0, "Banker Pair": 0, "Lucky 6": 0}
            self.round_net_profit = 0
            self.place_bets()
            time.sleep(1)
            self.play_hand()
            dec = input(f"{colors.CYAN}Do you want to keep playing (Y/N)?{colors.RESET}").lower()
            if dec != "y":
                break

game = Baccarat()
game.start_game()
