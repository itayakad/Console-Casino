from misc.deck import Deck
from misc.hand_evaluator import HandEvaluator
import time

deck = Deck()

# Function to shuffle and deal cards
def shuffle_deal(deck):
    player1_hand = deck.deal(2)
    player2_hand = deck.deal(2)
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
        print(f"CA:{call_amount}, HB: {hero_bet}, VB: {villain_bet}")
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

class AIPlayer(Player):
    def __init__(self, name, chips):
        super().__init__(name, chips)
    
    def bot_raise(self):
        self.bet(50)
        return 50

    def make_decision(self, community_cards, pot, opponent_bet, type):
        time.sleep(1)
        '''evaluator = HandEvaluator()
        best_hand = evaluator.best_hand(self.hand, community_cards)
        hand_strength = evaluator.evaluate_hand_strength(best_hand)'''

        if type == 1:
            return "check"
        if type == 2:
            return "call"
        if type == 3:
            return "raise"

def display_game_state(player1, player2, pot, community_cards, flip):
    print("\n--- Game State ---")
    if flip:
        print(f"{player1.name}'s Hand: {player1.hand}")
        print(f"{player2.name}'s Hand: {player2.hand}")
    else:
        if not isinstance(player1, AIPlayer):
            print(f"{player1.name}'s Hand: {player1.hand}")
        else:
            print(f"{player2.name}'s Hand: {player2.hand}")
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
                        if isinstance(player1, AIPlayer):
                            action = player1.make_decision(community_cards, pot, player2.current_bet, 1)
                            break
                        else:
                            action = input(f"{player1.name}, choose your action (check, raise): ").lower()
                            if action in ['check', 'raise']:
                                break
                            else:
                                print("Invalid action. Please choose 'check' or 'raise'.")
                    elif player2.current_bet >= player1.chips:
                        if isinstance(player1, AIPlayer):
                            action = player1.make_decision(community_cards, pot, player2.current_bet, 2)
                            break
                        else:
                            action = input(f"{player1.name}, choose your action (call {player2.current_bet - player1.current_bet}, fold): ").lower()
                            if action in ['call', 'fold']:
                                break
                            else:
                                print("Invalid action. Please choose 'call' or 'fold'.")
                    else:
                        if isinstance(player1, AIPlayer):
                            action = player1.make_decision(community_cards, pot, player2.current_bet, 3)
                            break
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
                    if isinstance(player1, AIPlayer):
                        raise_amount = player1.bot_raise()
                    else:
                        raise_amount = player1.raise_bet(player2)
                    print(f"{player1.name} has raised {raise_amount}.")
                    pot += raise_amount
                    player1_acted = True
                    player2_acted = False
                        
            # Player 2's turn
            if not player2_acted:
                while True:
                    if player2.current_bet == player1.current_bet:
                        if isinstance(player2, AIPlayer):
                            action = player2.make_decision(community_cards, pot, player1.current_bet, 1)
                            print(1)
                            break
                        else:
                            action = input(f"{player2.name}, choose your action (check, raise): ").lower()
                            if action in ['check', 'raise']:
                                break
                            else:
                                print("Invalid action. Please choose 'check' or 'raise'.")
                    elif player1.current_bet >= player2.chips:
                        if isinstance(player2, AIPlayer):
                            action = player2.make_decision(community_cards, pot, player1.current_bet, 2)
                            print(2)
                            break
                        else:
                            action = input(f"{player2.name}, choose your action (call {player1.current_bet - player2.current_bet}, fold): ").lower()
                            if action in ['call', 'fold']:
                                break
                            else:
                                print("Invalid action. Please choose 'call' or 'fold'.")
                    else:
                        if isinstance(player2, AIPlayer):
                            action = player2.make_decision(community_cards, pot, player1.current_bet, 3)
                            print("3")
                            break
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
                    if isinstance(player2, AIPlayer):
                        raise_amount = player2.bot_raise
                    else:
                        raise_amount = player2.raise_bet(player1)
                    print(f"{player2.name} has raised {raise_amount}.")
                    pot += raise_amount
                    player2_acted = True
                    player1_acted = False

            # End the betting round if both players have acted and bets are equal
            if player1_acted and player2_acted and player1.current_bet == player2.current_bet:
                break

    return pot

def compare_hands(hand1, hand2, community_cards):
    evaluator = HandEvaluator()
    best_hand1 = evaluator.best_hand(hand1, community_cards)
    best_hand2 = evaluator.best_hand(hand2, community_cards)

    print(f"{player1.name} Best Hand: {best_hand1}")
    print(f"{player2.name} Best Hand: {best_hand2}")

    hand_type1 = evaluator.hand_type(best_hand1[0])
    hand_type2 = evaluator.hand_type(best_hand2[0])

    if best_hand1[0] > best_hand2[0]:
        print(f"{player1.name}'s {hand_type1} beats {player2.name}'s {hand_type2}")
        return player1
    elif best_hand1[0] < best_hand2[0]:
        print(f"{player2.name}'s {hand_type2} beats {player1.name}'s {hand_type1}")
        return player2
    else:
        # Compare the card ranks in the best hands
        for card1, card2 in zip(best_hand1[1], best_hand2[1]):
            rank1 = evaluator.card_rank(card1)
            rank2 = evaluator.card_rank(card2)
            if rank1 > rank2:
                print(f"{player1.name}'s {hand_type1} beats {player2.name}'s {hand_type2}")
                return player1
            elif rank1 < rank2:
                print(f"{player2.name}'s {hand_type2} beats {player1.name}'s {hand_type1}")
                return player2
        print("It's a tie")
        return

name = input("What is your name?: ").capitalize()
buyin = int(input("How much would you like to buy in? This determines the blinds of the game as well: "))
print(f"Welcome, {name}. You will be playing against an AI Poker Bot in heads up poker. You have chosen to buy in for {buyin}. The bot will match this stack, and the blinds are set at {buyin/100}/{buyin/50}.")

# Initialize players
player1 = Player(name, buyin)
player2 = AIPlayer("Bot", buyin)
player1.current_bet = 0
player2.current_bet = 0
SMALL_BLIND = buyin/100
BIG_BLIND = buyin/50
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
    display_game_state(player1, player2, pot, community_cards, False)
    
    # Run betting rounds and deal community cards
    pot = betting_round(first_actor, first_actor_bet, second_actor, second_actor_bet, pot, True)  # First betting round
    community_cards.extend(deck.deal(3))  # Deal the flop (3 cards)
    display_game_state(player1, player2, pot, community_cards, False)
    pot = betting_round(first_actor, 0, second_actor, 0, pot, False)  # Betting round after flop

    community_cards.extend(deck.deal(1))  # Deal the turn (1 card)
    display_game_state(player1, player2, pot, community_cards, False)
    pot = betting_round(first_actor, 0, second_actor, 0, pot, False)  # Betting round after turn

    community_cards.extend(deck.deal(1))  # Deal the river (1 card)
    display_game_state(player1, player2, pot, community_cards, False)
    pot = betting_round(first_actor, 0, second_actor, 0, pot, False)  # Final betting round

    # Display final game state
    display_game_state(player1, player2, pot, community_cards, True)

    # Determine and display the winner
    if player1.folded:
        player2.chips += pot
        print("Player 2 wins because Player 1 folded.")
    elif player2.folded:
        player1.chips += pot
        print("Player 1 wins because Player 2 folded.")
    else:
        winner = compare_hands(player1.hand, player2.hand, community_cards)
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
