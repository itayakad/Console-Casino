import random
from collections import Counter

# Define the suits and ranks of a standard deck of cards
suits = ['♣', '♦', '♥', '♠']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Create the deck of cards
deck = [f"{rank}{suit}" for suit in suits for rank in ranks]

# Function to shuffle and deal cards
def shuffle_deal(deck):
    random.shuffle(deck)
    player1_hand = [deck.pop(), deck.pop()]
    player2_hand = [deck.pop(), deck.pop()]
    return player1_hand, player2_hand, deck

class Player:
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = []
        self.current_bet = 0
        self.folded = False

    def bet(self, amount):
        self.chips -= amount
        self.current_bet += amount

    def fold(self):
        self.folded = True

    def check(self):
        pass

    def call(self, hero_bet, villain_bet):
        call_amount = villain_bet - hero_bet
        #print(f"CA:{call_amount}, HB: {hero_bet}, VB: {villain_bet}")
        self.bet(call_amount)
        return call_amount

    def raise_bet(self, villain):
        invalid_value = True
        while invalid_value:
            raise_input = input("Enter raise amount (enter 'all in' to go all in): ")
            if raise_input.lower() == "all in":
                invalid_value = False
            elif raise_input.isdigit() and int(raise_input) >= 2 * villain.current_bet:
                invalid_value = False
            else:
                print(f"Invalid input. You must bet at least twice the opponent's bet ({villain.current_bet}), so min raise is {villain.current_bet * 2}")
        
        if raise_input.lower() == "all in":
            if self.chips > villain.chips:
                print(f"{self.name} has gone all in. Since {villain.name} has less chips, the all in amount is set at {villain.name}'s stack, so {self.name} goes all in for {villain.chips}.")
                raise_amount = villain.chips + (villain.current_bet - self.current_bet)
            else:
                raise_amount = self.chips
        else:
            raise_amount = int(raise_input)
            #print(f"Raise:{raise_amount}")
        
        self.bet(raise_amount)
        return raise_amount

def display_game_state(player1, player2, pot, community_cards):
    print("\n--- Game State ---")
    print(f"{player1.name} Hand: {player1.hand}")
    print(f"{player2.name} Hand: {player2.hand}")
    print(f"Community Cards: {community_cards}")
    print(f"Pot Size: {pot}")
    print(f"{player1.name} Chips: {player1.chips}")
    print(f"{player2.name} Chips: {player2.chips}")
    print("------------------\n")

def betting_round(player1, player1_bet, player2, player2_bet, pot, blinds):
    if (not player1.folded and not player2.folded) and (player1.chips > 0 and player2.chips > 0):
        player1_acted = False
        player2_acted = False
        player1.current_bet = player1_bet
        player2.current_bet = player2_bet
        while True:
            # Player 1's turn
            if not player1_acted:
                while True:
                    if player1.current_bet == player2.current_bet:
                        action = input(f"{player1.name}, choose your action (check, raise): ").lower()
                        if action in ['check', 'raise']:
                            break
                        else:
                            print("Invalid action. Please choose 'check' or 'raise'.")
                    elif player2.current_bet >= player1.chips:
                        action = input(f"{player1.name}, choose your action (call {player2.current_bet - player1.current_bet}, fold): ").lower()
                        if action in ['call', 'fold']:
                            break
                        else:
                            print("Invalid action. Please choose 'call' or 'fold'.")
                    else:
                        action = input(f"{player1.name}, choose your action (call {player2.current_bet - player1.current_bet}, raise, fold): ").lower()
                        if action in ['call', 'raise', 'fold']:
                            break
                        else:
                            print("Invalid action. Please choose 'call', 'raise', or 'fold'.")

                if action == 'fold':
                    print(f"{player1.name} has folded.")
                    player1.fold()
                    player1_acted = True
                    break
                elif action == 'check':
                    print(f"{player1.name} has checked.")
                    player1.check()
                    player1_acted = True
                elif action == 'call':
                    call_amount = player1.call(player1.current_bet, player2.current_bet)
                    print(f"{player1.name} has called {call_amount}.")
                    pot += call_amount
                    player1_acted = True
                    if not blinds:
                        player2_acted = True
                elif action == 'raise':
                    raise_amount = player1.raise_bet(player2)
                    print(f"{player1.name} has raised {raise_amount}.")
                    pot += raise_amount
                    player1_acted = True
                    player2_acted = False
                        
            # Player 2's turn
            if not player2_acted:
                while True:
                    if player2.current_bet == player1.current_bet:
                        action = input(f"{player2.name}, choose your action (check, raise): ").lower()
                        if action in ['check', 'raise']:
                            break
                        else:
                            print("Invalid action. Please choose 'check' or 'raise'.")
                    elif player1.current_bet >= player2.chips:
                        action = input(f"{player2.name}, choose your action (call {player1.current_bet - player2.current_bet}, fold): ").lower()
                        if action in ['call', 'fold']:
                            break
                        else:
                            print("Invalid action. Please choose 'call' or 'fold'.")
                    else:
                        action = input(f"{player2.name}, choose your action (call {player1.current_bet - player2.current_bet}, raise, fold): ").lower()
                        if action in ['call', 'raise', 'fold']:
                            break
                        else:
                            print("Invalid action. Please choose 'call', 'raise', or 'fold'.")

                if action == 'fold':
                    print(f"{player2.name} has folded.")
                    player2.fold()
                    player2_acted = True
                    break
                elif action == 'check':
                    print(f"{player2.name} has checked.")
                    player2.check()
                    player2_acted = True
                elif action == 'call':
                    call_amount = player2.call(player2.current_bet, player1.current_bet)
                    print(f"{player2.name} has called {call_amount}.")
                    pot += call_amount
                    player2_acted = True
                    if not blinds:
                        player1_acted = True
                elif action == 'raise':
                    raise_amount = player2.raise_bet(player1)
                    print(f"{player2.name} has raised {raise_amount}.")
                    pot += raise_amount
                    player2_acted = True
                    player1_acted = False

            # End the betting round if both players have acted and bets are equal
            if player1_acted and player2_acted and player1.current_bet == player2.current_bet:
                break

    return pot

class HandEvaluator:
    def __init__(self):
        pass

    @staticmethod
    def hand_type(hand_rank):
        hand_types = ["High Card", "One Pair", "Two Pair", "Three of a Kind", "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush"]
        return hand_types[hand_rank]

    @staticmethod
    def card_rank(card):
        rank = card[:-1]  # Everything except the last character is the rank
        if rank == 'A':
            return 14
        elif rank == 'K':
            return 13
        elif rank == 'Q':
            return 12
        elif rank == 'J':
            return 11
        else:
            return int(rank)

    @staticmethod
    def card_suit(card):
        return card[-1]  # The last character is the suit

    @staticmethod
    def is_straight_flush(hand):
        suits = [HandEvaluator.card_suit(card) for card in hand]
        ranks = sorted([HandEvaluator.card_rank(card) for card in hand])
        return len(set(suits)) == 1 and ranks == list(range(min(ranks), min(ranks) + 5))

    @staticmethod
    def is_four_of_a_kind(hand):
        ranks = [HandEvaluator.card_rank(card) for card in hand]
        return 4 in Counter(ranks).values()

    @staticmethod
    def is_full_house(hand):
        ranks = [HandEvaluator.card_rank(card) for card in hand]
        counter = Counter(ranks).values()
        return 3 in counter and 2 in counter

    @staticmethod
    def is_flush(hand):
        suits = [HandEvaluator.card_suit(card) for card in hand]
        return len(set(suits)) == 1

    @staticmethod
    def is_straight(hand):
        ranks = sorted([HandEvaluator.card_rank(card) for card in hand])
        return ranks == list(range(min(ranks), min(ranks) + 5))

    @staticmethod
    def is_three_of_a_kind(hand):
        ranks = [HandEvaluator.card_rank(card) for card in hand]
        return 3 in Counter(ranks).values()

    @staticmethod
    def is_two_pair(hand):
        ranks = [HandEvaluator.card_rank(card) for card in hand]
        counter = Counter(ranks).values()
        return len([count for count in counter if count == 2]) == 2

    @staticmethod
    def is_one_pair(hand):
        ranks = [HandEvaluator.card_rank(card) for card in hand]
        return 2 in Counter(ranks).values()

    @staticmethod
    def best_hand(player_hand, community_cards):
        all_cards = player_hand + community_cards
        best = []
        best_rank = (0, [])

        for i in range(len(all_cards)):
            for j in range(i + 1, len(all_cards)):
                for k in range(j + 1, len(all_cards)):
                    for l in range(k + 1, len(all_cards)):
                        for m in range(l + 1, len(all_cards)):
                            hand = [all_cards[i], all_cards[j], all_cards[k], all_cards[l], all_cards[m]]
                            current_best_rank = (0, sorted(hand, key=lambda x: HandEvaluator.card_rank(x), reverse=True))

                            if HandEvaluator.is_straight_flush(hand):
                                current_best_rank = (8, sorted(hand, key=lambda x: HandEvaluator.card_rank(x), reverse=True))
                            elif HandEvaluator.is_four_of_a_kind(hand):
                                current_best_rank = (7, sorted(hand, key=lambda x: HandEvaluator.card_rank(x), reverse=True))
                            elif HandEvaluator.is_full_house(hand):
                                current_best_rank = (6, sorted(hand, key=lambda x: HandEvaluator.card_rank(x), reverse=True))
                            elif HandEvaluator.is_flush(hand):
                                current_best_rank = (5, sorted(hand, key=lambda x: HandEvaluator.card_rank(x), reverse=True))
                            elif HandEvaluator.is_straight(hand):
                                current_best_rank = (4, sorted(hand, key=lambda x: HandEvaluator.card_rank(x), reverse=True))
                            elif HandEvaluator.is_three_of_a_kind(hand):
                                current_best_rank = (3, sorted(hand, key=lambda x: HandEvaluator.card_rank(x), reverse=True))
                            elif HandEvaluator.is_two_pair(hand):
                                current_best_rank = (2, sorted(hand, key=lambda x: HandEvaluator.card_rank(x), reverse=True))
                            elif HandEvaluator.is_one_pair(hand):
                                current_best_rank = (1, sorted(hand, key=lambda x: HandEvaluator.card_rank(x), reverse=True))
                            else:
                                current_best_rank = (0, sorted(hand, key=lambda x: HandEvaluator.card_rank(x), reverse=True))

                            best_rank = max(best_rank, current_best_rank, key=lambda x: (x[0], [HandEvaluator.card_rank(card) for card in x[1]]))

        return best_rank

    @staticmethod
    def compare_hands(hand1, hand2, community_cards):
        best_hand1 = HandEvaluator.best_hand(hand1, community_cards)
        best_hand2 = HandEvaluator.best_hand(hand2, community_cards)

        print(f"{player1.name} Best Hand: {best_hand1}")
        print(f"{player2.name} Best Hand: {best_hand2}")

        hand_type1 = HandEvaluator.hand_type(best_hand1[0])
        hand_type2 = HandEvaluator.hand_type(best_hand2[0])

        if best_hand1[0] > best_hand2[0]:
            print(f"{player1.name}'s {hand_type1} beats {player2.name}'s {hand_type2}")
            return player1
        elif best_hand1[0] < best_hand2[0]:
            print(f"{player2.name}'s {hand_type2} beats {player1.name}'s {hand_type1}")
            return player2
        else:
            # Compare the card ranks in the best hands
            for card1, card2 in zip(best_hand1[1], best_hand2[1]):
                rank1 = HandEvaluator.card_rank(card1)
                rank2 = HandEvaluator.card_rank(card2)
                if rank1 > rank2:
                    print(f"{player1.name}'s {hand_type1} beats {player2.name}'s {hand_type2}")
                    return player1
                elif rank1 < rank2:
                    print(f"{player2.name}'s {hand_type2} beats {player1.name}'s {hand_type1}")
                    return player2
            print("It's a tie")
            return

# Initialize players
player1 = Player("Player 1", 1000)
player2 = Player("Player 2", 1000)
player1.current_bet = 0
player2.current_bet = 0
SMALL_BLIND = 10
BIG_BLIND = 20
hand_num = 0

# Initialize dealer
dealer = player1

while player1.chips > 0 and player2.chips > 0:
    # Reset the pot and deal new cards
    hand_num = hand_num + 1
    pot = 0
    player1.folded = False
    player2.folded = False
    player1.hand, player2.hand, deck = shuffle_deal(deck)  # Deal new cards
    community_cards = []  # Reset community cards

    # Determine who acts first based on the dealer
    if dealer == player1:
        first_actor, first_actor_bet, second_actor, second_actor_bet = player2, SMALL_BLIND, player1, BIG_BLIND  # Player 2 acts first
    else:
        first_actor, first_actor_bet, second_actor, second_actor_bet = player1, SMALL_BLIND, player2, BIG_BLIND  # Player 1 acts first

    # Display initial game state
    print(f"Hand {hand_num}:\n{player1.name}'s stack: {player1.chips}.\n{player2.name}'s stack: {player2.chips}.")
    print(f"{first_actor.name} is the Small Blind ({SMALL_BLIND}), {second_actor.name} is the Big Blind ({BIG_BLIND}).\n{first_actor.name} acts first.")
    first_actor.chips -= SMALL_BLIND
    second_actor.chips -= BIG_BLIND
    pot += SMALL_BLIND + BIG_BLIND
    display_game_state(player1, player2, pot, community_cards)
    
    # Run betting rounds and deal community cards
    pot = betting_round(first_actor, first_actor_bet, second_actor, second_actor_bet, pot, True)  # First betting round
    community_cards.extend([deck.pop(), deck.pop(), deck.pop()])  # Deal the flop (3 cards)
    display_game_state(player1, player2, pot, community_cards)
    pot = betting_round(first_actor, 0, second_actor, 0, pot, False)  # Betting round after flop

    community_cards.append(deck.pop())  # Deal the turn (1 card)
    display_game_state(player1, player2, pot, community_cards)
    pot = betting_round(first_actor, 0, second_actor, 0, pot, False)  # Betting round after turn

    community_cards.append(deck.pop())  # Deal the river (1 card)
    display_game_state(player1, player2, pot, community_cards)
    pot = betting_round(first_actor, 0, second_actor, 0, pot, False)  # Final betting round

    # Display final game state
    display_game_state(player1, player2, pot, community_cards)

    # Determine and display the winner
    if player1.folded:
        player2.chips += pot
        print("Player 2 wins because Player 1 folded.")
    elif player2.folded:
        player1.chips += pot
        print("Player 1 wins because Player 2 folded.")
    else:
        evaluator = HandEvaluator()
        winner = evaluator.compare_hands(player1.hand, player2.hand, community_cards)
        if winner == player1:
            player1.chips += pot
        elif winner == player2:
            player2.chips += pot
        else:
            player1.chips += int(pot/2)
            player2.chips += int(pot/2)

    # Alternate the dealer for the next hand
    print(f"{player1.name}'s stack: {player1.chips}.\n{player2.name}'s stack: {player2.chips}.")
    dealer = player2 if dealer == player1 else player1

    # Check if the game should continue
    if player1.chips == 0 and player2.chips > 0:
        print(f"Game over! {player2.name} wins!")
        break
    elif player2.chips ==0 and player1.chips > 0:
        print(f"Game over! {player1.name} wins!")
        break

    continue_game = input(f"Do you want to play another hand? (yes/no): ").lower()
    if continue_game != 'yes':
        break