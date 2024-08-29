import time
from misc.deck import Deck
import misc.ansicolors as colors

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
        print(f"{colors.CYAN}{name}'s hand:{colors.RESET} {', '.join(map(str, hand[:-1]))}, [Hidden]")
    else:
        print(f"{colors.CYAN}{name}'s hand:{colors.RESET} {', '.join(map(str, hand))} (Value: {hand_value_display})")

def hit(deck, hand):
    hand.append(deck.deal(1)[0])
    print_hand(hand, "Player")
    if calculate_hand_value(hand) > 21:
        print(f"{colors.RED}You bust! Dealer wins.{colors.RESET}")
        return False
    return True

def stand(hand):
    print(f"{colors.YELLOW}You stand with a hand value of {display_hand_value(hand)}.{colors.RESET}")
    return True

def split_hand(deck, hand, bet):
    if hand[0].rank != hand[1].rank:
        print(f"{colors.RED}You cannot split this hand.{colors.RESET}")
        return None, None, None

    hand1 = [hand[0], deck.deal(1)[0]]
    time.sleep(1)
    hand2 = [hand[1], deck.deal(1)[0]]
    time.sleep(1)

    print(f"{colors.MAGENTA}Hand 1 after split:{colors.RESET}")
    print_hand(hand1, "Player's Hand 1")
    print(f"{colors.MAGENTA}Hand 2 after split:{colors.RESET}")
    print_hand(hand2, "Player's Hand 2")

    bet2 = bet

    while True:
        choice = input(f"{colors.YELLOW}Hand 1: Do you want to (H)it or (S)tand? {colors.RESET}").lower()
        if choice == 'h':
            if not hit(deck, hand1):
                break
        elif choice == 's':
            stand(hand1)
            break
        else:
            print(f"{colors.RED}Invalid choice. Please choose 'H' to Hit or 'S' to Stand.{colors.RESET}")

    while True:
        choice = input(f"{colors.YELLOW}Hand 2: Do you want to (H)it or (S)tand? {colors.RESET}").lower()
        if choice == 'h':
            if not hit(deck, hand2):
                break
        elif choice == 's':
            stand(hand2)
            break
        else:
            print(f"{colors.RED}Invalid choice. Please choose 'H' to Hit or 'S' to Stand.{colors.RESET}")

    return hand1, hand2, bet2

def double_down(deck, hand):
    print(f"{colors.CYAN}You chose to double down.{colors.RESET}")
    face_choice = input(f"{colors.CYAN}Do you want the card to be dealt face up (U) or face down (D)? {colors.RESET}").lower()
    
    hand.append(deck.deal(1)[0])
    
    if face_choice == 'd':
        print_hand(hand, "Player", hide_last_card=True)
    else:
        print_hand(hand, "Player")
    
    return hand

def offer_insurance(bet, dealer_hand):
    if dealer_hand[0].rank == 'A':
        insurance_bet = input(f"{colors.YELLOW}Dealer has an Ace. Do you want to take insurance? (Y/N) {colors.RESET}").lower()
        if insurance_bet == 'y':
            insurance_amount = min(bet // 2, bet)
            return insurance_amount
    return 0

def should_offer_surrender(dealer_hand):
    return dealer_hand[0].rank in ['A', '10', 'J', 'Q', 'K']

def surrender(bet):
    surrender_choice = input(f"{colors.MAGENTA}Do you want to surrender and lose half your bet (${bet // 2})? (Y/N) {colors.RESET}").lower()
    if surrender_choice == 'y':
        print(f"{colors.MAGENTA}You have surrendered. You lose ${bet // 2}.{colors.RESET}")
        return True
    return False

def blackjack():
    net = 0
    playing = True
    play_again = 'c'

    while playing:
        if play_again == 'c':
            bet = int(input(f"\n{colors.CYAN}How many $$ would you like to bet?: {colors.RESET}$"))

        deck = Deck()
        player_hand = deck.deal(2)
        dealer_hand = deck.deal(2)

        print_hand(player_hand, "Player")
        print(f"{colors.CYAN}Dealer's hand:{colors.RESET} {dealer_hand[0]}, [Hidden]")

        insurance_amount = offer_insurance(bet, dealer_hand)
        if insurance_amount > 0:
            print(f"{colors.YELLOW}Insurance bet placed: ${insurance_amount}{colors.RESET}")

        if should_offer_surrender(dealer_hand) and surrender(bet):
            net -= bet // 2
            continue

        if dealer_hand[0].rank == 'A':
            # Check if the dealer could have a blackjack
            if any(card.rank in ['10', 'J', 'Q', 'K'] for card in dealer_hand[1:]):
                print(f"{colors.CYAN}Dealer flips their other card...{colors.RESET}")
                time.sleep(2)  # Pause for dramatic effect
                print_hand(dealer_hand, "Dealer")

                if calculate_hand_value(dealer_hand) == 21:
                    print(f"{colors.RED}Dealer has Blackjack!{colors.RESET}")
                    if insurance_amount > 0:
                        print(f"{colors.GREEN}Insurance pays 2 to 1.{colors.RESET}")
                        net += insurance_amount * 2
                    net -= bet
                    continue
            else:
                print(f"{colors.YELLOW}Dealer does not have a Blackjack.{colors.RESET}")

        can_split = player_hand[0].rank == player_hand[1].rank
        doubled_down = False

        while playing:
            choice = input(f"{colors.CYAN}Do you want to hit (h), stand (s), split (p), or double down (d)? {colors.RESET}").lower()
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
                        print(f"{colors.GREEN}Hand 1 wins!{colors.RESET}")
                        net += bet
                    else:
                        print(f"{colors.RED}Hand 1 loses!{colors.RESET}")
                        net -= bet

                    if player_value2 > dealer_hand_value and player_value2 <= 21:
                        print(f"{colors.GREEN}Hand 2 wins!{colors.RESET}")
                        net += bet2
                    else:
                        print(f"{colors.RED}Hand 2 loses!{colors.RESET}")
                        net -= bet2

                    break
            elif choice == 'd':
                player_hand = double_down(deck, player_hand)
                doubled_down = True
                break
            else:
                print(f"{colors.RED}Invalid choice or cannot split. Please choose 'H', 'S', 'P', or 'D'.{colors.RESET}")

        # Dealer's turn
        if calculate_hand_value(player_hand) <= 21:
            print_hand(dealer_hand, "Dealer")
            while calculate_hand_value(dealer_hand) < 17:
                dealer_hand.append(deck.deal(1)[0])
                time.sleep(2)  # Pause for 2 seconds
                print_hand(dealer_hand, "Dealer")
                if calculate_hand_value(dealer_hand) > 21:
                    print(f"{colors.GREEN}Dealer busts! You win!{colors.RESET}")
                    net += bet * (2 if doubled_down else 1)
                    break

            dealer_value = calculate_hand_value(dealer_hand)
            if dealer_value <= 21:  # This condition is now updated to use the correct value
                if doubled_down:
                    print(f"{colors.CYAN}Revealing your hidden card...{colors.RESET}")
                    time.sleep(2)
                    print_hand(player_hand, "Player")

                player_value = calculate_hand_value(player_hand)

                if player_value > dealer_value:
                    print(f"{colors.GREEN}You win!{colors.RESET}")
                    net += bet * (2 if doubled_down else 1)
                elif player_value < dealer_value:
                    print(f"{colors.RED}Dealer wins!{colors.RESET}")
                    net -= bet * (2 if doubled_down else 1)
                else:
                    print(f"{colors.YELLOW}It's a tie!{colors.RESET}")

        # Resolve insurance bet
        if insurance_amount > 0:
            if calculate_hand_value(dealer_hand) == 21:
                print(f"{colors.GREEN}Dealer has Blackjack! Insurance pays 2 to 1.{colors.RESET}")
                net += insurance_amount * 2
            else:
                print(f"{colors.RED}Dealer does not have Blackjack. You lose the insurance bet.{colors.RESET}")
                net -= insurance_amount

        while True:
            play_again = input(f"{colors.CYAN}Do you want to stop (s), play again with the same bet of ${bet} (r), or change your bet (c)?\n If you would like to see how you are doing so far, enter 'net': {colors.RESET}").lower()
            if play_again == 'net':
                print(f"{colors.BLUE}Your net profit is ${net}.{colors.RESET}")
            elif play_again == 's':
                print(f"{colors.BLUE}Thanks for playing! Your net profit is ${net}.{colors.RESET}")
                playing = False
                break
            else:
                break

if __name__ == "__main__":
    blackjack()
