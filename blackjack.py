import time
from misc.deck import Deck

# Define ANSI escape codes for colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"

def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        if card.rank in ['J', 'Q', 'K']:
            value += 10
        elif card.rank == 'A':
            aces += 1
            value += 11
        else:
            value += int(card.rank)
    
    # Adjust for aces if value exceeds 21
    while value > 21 and aces:
        value -= 10
        aces -= 1
    
    return value

def display_hand_value(hand):
    value = calculate_hand_value(hand)
    if any(card.rank == 'A' for card in hand):
        secondary_value = value - 10 if value > 21 else value
        if value != secondary_value:
            return f"{secondary_value}/{value}" if secondary_value <= 21 else f"{secondary_value}"
    return str(value)

def print_hand(hand, name, hide_last_card=False):
    hand_value_display = display_hand_value(hand)
    if hide_last_card:
        print(f"{CYAN}{name}'s hand:{RESET} {', '.join(map(str, hand[:-1]))}, [Hidden]")
    else:
        print(f"{CYAN}{name}'s hand:{RESET} {', '.join(map(str, hand))} (Value: {hand_value_display})")

def hit(deck, hand):
    hand.append(deck.deal(1)[0])
    print_hand(hand, "Player")
    if calculate_hand_value(hand) > 21:
        print(f"{RED}You bust! Dealer wins.{RESET}")
        return False
    return True

def stand(hand):
    print(f"{YELLOW}You stand with a hand value of {display_hand_value(hand)}.{RESET}")
    return True

def split_hand(deck, hand, bet):
    if hand[0].rank != hand[1].rank:
        print(f"{RED}You cannot split this hand.{RESET}")
        return None, None, None

    hand1 = [hand[0], deck.deal(1)[0]]
    time.sleep(1)
    hand2 = [hand[1], deck.deal(1)[0]]
    time.sleep(1)

    print(f"{MAGENTA}Hand 1 after split:{RESET}")
    print_hand(hand1, "Player's Hand 1")
    print(f"{MAGENTA}Hand 2 after split:{RESET}")
    print_hand(hand2, "Player's Hand 2")

    bet2 = bet

    while True:
        choice = input(f"{YELLOW}Hand 1: Do you want to (H)it or (S)tand? {RESET}").lower()
        if choice == 'h':
            if not hit(deck, hand1):
                break
        elif choice == 's':
            stand(hand1)
            break
        else:
            print(f"{RED}Invalid choice. Please choose 'H' to Hit or 'S' to Stand.{RESET}")

    while True:
        choice = input(f"{YELLOW}Hand 2: Do you want to (H)it or (S)tand? {RESET}").lower()
        if choice == 'h':
            if not hit(deck, hand2):
                break
        elif choice == 's':
            stand(hand2)
            break
        else:
            print(f"{RED}Invalid choice. Please choose 'H' to Hit or 'S' to Stand.{RESET}")

    return hand1, hand2, bet2

def double_down(deck, hand):
    print(f"{CYAN}You chose to double down.{RESET}")
    face_choice = input(f"{CYAN}Do you want the card to be dealt face up (U) or face down (D)? {RESET}").lower()
    
    hand.append(deck.deal(1)[0])
    
    if face_choice == 'd':
        print_hand(hand, "Player", hide_last_card=True)
    else:
        print_hand(hand, "Player")
    
    return hand

def offer_insurance(bet, dealer_hand):
    if dealer_hand[0].rank == 'A':
        insurance_bet = input(f"{YELLOW}Dealer has an Ace. Do you want to take insurance? (Y/N) {RESET}").lower()
        if insurance_bet == 'y':
            insurance_amount = min(bet // 2, bet)
            return insurance_amount
    return 0

def should_offer_surrender(dealer_hand):
    return dealer_hand[0].rank in ['A', '10', 'J', 'Q', 'K']

def surrender(bet):
    surrender_choice = input(f"{MAGENTA}Do you want to surrender and lose half your bet (${bet // 2})? (Y/N) {RESET}").lower()
    if surrender_choice == 'y':
        print(f"{MAGENTA}You have surrendered. You lose ${bet // 2}.{RESET}")
        return True
    return False

def blackjack():
    net = 0
    playing = True
    play_again = 'c'

    while playing:
        if play_again == 'c':
            bet = int(input(f"\n{CYAN}How many $$ would you like to bet?: {RESET}$"))

        deck = Deck()
        player_hand = deck.deal(2)
        dealer_hand = deck.deal(2)

        print_hand(player_hand, "Player")
        print(f"{CYAN}Dealer's hand:{RESET} {dealer_hand[0]}, [Hidden]")

        insurance_amount = offer_insurance(bet, dealer_hand)
        if insurance_amount > 0:
            print(f"{YELLOW}Insurance bet placed: ${insurance_amount}{RESET}")

        if should_offer_surrender(dealer_hand) and surrender(bet):
            net -= bet // 2
            continue

        if dealer_hand[0].rank == 'A':
            # Check if the dealer could have a blackjack
            if any(card.rank in ['10', 'J', 'Q', 'K'] for card in dealer_hand[1:]):
                print(f"{CYAN}Dealer flips their other card...{RESET}")
                time.sleep(2)  # Pause for dramatic effect
                print_hand(dealer_hand, "Dealer")

                if calculate_hand_value(dealer_hand) == 21:
                    print(f"{RED}Dealer has Blackjack!{RESET}")
                    if insurance_amount > 0:
                        print(f"{GREEN}Insurance pays 2 to 1.{RESET}")
                        net += insurance_amount * 2
                    net -= bet
                    continue
            else:
                print(f"{YELLOW}Dealer does not have a Blackjack.{RESET}")

        can_split = player_hand[0].rank == player_hand[1].rank
        doubled_down = False

        while playing:
            choice = input(f"{CYAN}Do you want to hit (h), stand (s), split (p), or double down (d)? {RESET}").lower()
            if choice == 'h':
                if not hit(deck, player_hand):
                    net -= bet
                    break
            elif choice == 's':
                stand(player_hand)
                break
            elif choice == 'p' and can_split:
                hand1, hand2, bet2 = split_hand(deck, player_hand, bet)
                if hand1 and hand2:
                    dealer_hand_value = calculate_hand_value(dealer_hand)
                    player_value1 = calculate_hand_value(hand1)
                    player_value2 = calculate_hand_value(hand2)

                    if player_value1 > dealer_hand_value and player_value1 <= 21:
                        print(f"{GREEN}Hand 1 wins!{RESET}")
                        net += bet
                    else:
                        print(f"{RED}Hand 1 loses!{RESET}")
                        net -= bet

                    if player_value2 > dealer_hand_value and player_value2 <= 21:
                        print(f"{GREEN}Hand 2 wins!{RESET}")
                        net += bet2
                    else:
                        print(f"{RED}Hand 2 loses!{RESET}")
                        net -= bet2

                    break
            elif choice == 'd':
                player_hand = double_down(deck, player_hand)
                doubled_down = True
                break
            else:
                print(f"{RED}Invalid choice or cannot split. Please choose 'H', 'S', 'P', or 'D'.{RESET}")

        # Dealer's turn
        if calculate_hand_value(player_hand) <= 21:
            print_hand(dealer_hand, "Dealer")
            while calculate_hand_value(dealer_hand) < 17:
                dealer_hand.append(deck.deal(1)[0])
                time.sleep(2)  # Pause for 2 seconds
                print_hand(dealer_hand, "Dealer")
                if calculate_hand_value(dealer_hand) > 21:
                    print(f"{GREEN}Dealer busts! You win!{RESET}")
                    net += bet * (2 if doubled_down else 1)
                    break

            dealer_value = calculate_hand_value(dealer_hand)
            if dealer_value <= 21:  # This condition is now updated to use the correct value
                if doubled_down:
                    print(f"{CYAN}Revealing your hidden card...{RESET}")
                    time.sleep(2)
                    print_hand(player_hand, "Player")

                player_value = calculate_hand_value(player_hand)

                if player_value > dealer_value:
                    print(f"{GREEN}You win!{RESET}")
                    net += bet * (2 if doubled_down else 1)
                elif player_value < dealer_value:
                    print(f"{RED}Dealer wins!{RESET}")
                    net -= bet * (2 if doubled_down else 1)
                else:
                    print(f"{YELLOW}It's a tie!{RESET}")

        # Resolve insurance bet
        if insurance_amount > 0:
            if calculate_hand_value(dealer_hand) == 21:
                print(f"{GREEN}Dealer has Blackjack! Insurance pays 2 to 1.{RESET}")
                net += insurance_amount * 2
            else:
                print(f"{RED}Dealer does not have Blackjack. You lose the insurance bet.{RESET}")
                net -= insurance_amount

        while True:
            play_again = input(f"{CYAN}Do you want to stop (s), play again with the same bet of ${bet} (r), or change your bet (c)?\n If you would like to see how you are doing so far, enter 'net': {RESET}").lower()
            if play_again == 'net':
                print(f"{BLUE}Your net profit is ${net}.{RESET}")
            elif play_again == 's':
                print(f"{BLUE}Thanks for playing! Your net profit is ${net}.{RESET}")
                playing = False
                break
            else:
                break

if __name__ == "__main__":
    blackjack()
