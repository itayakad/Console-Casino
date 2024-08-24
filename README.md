# ConsoleCasino
Contains various casino games like black jack, roulette, poker, and more. All games are meant to be able to be played fully in the terminal/console.

Summary of games:

**headsup_texasholdempoker.py** implements a heads-up poker game in Python, where a human player competes against an AI poker bot. The game manages player actions such as betting, folding, checking, calling, and raising, with betting rounds occurring after dealing community cards (flop, turn, river). The AI player has realistic logic for different scenarios. The script tracks the chips, pot, and alternates the dealer between rounds. The game continues until one player runs out of chips or the player decides to stop. The winner is determined by comparing the best hands after the final betting round.

**blackjack.py** implements a Blackjack game in Python, utilizing a deck of cards and ANSI colors for output formatting. It includes functions for handling player actions (such as hitting, standing, splitting, and doubling down), calculating hand values, offering insurance, and determining the outcome of the game. The main game loop prompts the player for inputs and manages the flow of the game, including betting and tracking net profits.

**jacksorbetter_videopoker.py** implements a Jacks or Better video poker game in Python, using a deck of cards and a hand evaluator to determine hand rankings and payouts. The game allows the player to bet any amount, hold specific cards, redraw the remaining cards, and calculates payouts based on the final hand's ranking. The player can continue playing with the same bet, change the bet size, or stop playing, with the game tracking net profits or losses.
