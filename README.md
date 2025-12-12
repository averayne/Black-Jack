# Blackjack

Command-line blackjack: object-oriented Card/Deck/Player classes, Fisher-Yates shuffle, insertion sort + binary search helpers, and a playable CLI with hit/stand/forfeit.

## About the game
- Goal: finish closer to 21 than the dealer without busting; natural blackjack (Ace + 10-value card) is best.
- Deal: player gets two face-up, dealer gets one face-up and one hidden.
- Dealer AI: hits until 17 and hits soft 17; otherwise stands.
- Player choices: hit, stand, or forfeit the round.

## Rules & logic
- Cards: 2-10 face value; J/Q/K = 10; Ace = 11 or 1.
- Win: higher total than dealer without busting, dealer bust, or natural blackjack when dealer does not match.
- Lose: player bust, dealer blackjack when player does not match, or lower total.
- Push: equal totals.
- Quit: choose forfeit in a round or answer `n` when prompted to play again.

## Algorithms used
- Fisher-Yates shuffle: unbiased in-place shuffle in `Deck.fisher_yates_shuffle`.
- Insertion sort: `insertion_sort` produces sorted player/dealer hands for display and search.
- Binary search: `binary_search_by_rank` (used by `Player.has_rank` and `Player.has_blackjack`) searches sorted hands by rank.

## Project structure
- `blackjack.py` - standalone CLI game and all supporting classes/algorithms.
- `README.md` - this file.

## How to run
1) Install Python 3.10+.
2) Open a terminal in the repo folder (where `blackjack.py` lives).
3) Run the game:
```bash
python blackjack.py
```
   - If you have multiple Python versions, use `python3 blackjack.py`.
4) Follow the prompts each hand:
   - `h` = hit (draw a card)
   - `s` = stand (end your turn)
   - `f` = forfeit the round
5) The dealer plays after you stand, then the outcome is shown. Type `y` to play again or `n` to quit.
   - The shoe auto-reshuffles when it runs low and will reshuffle mid-hand if a draw is attempted on an empty deck (very rare).

## What the script does
- Builds a standard 52-card deck and shuffles it with Fisher-Yates.
- Deals two cards to you and the dealer (dealer shows one).
- Lets you choose hit/stand/forfeit while showing your total and a sorted view of your hand.
- Dealer AI hits until 17 (hits soft 17), otherwise stands.
- Determines win/lose/push with blackjack detection and reshuffles when the shoe runs low.

## Sample playthrough
```
Dealer: 10 of Spades [hidden]
You: Queen of Clubs 3 of Spades (total: 13)
You: Queen of Clubs 3 of Spades (total: 13)
Sorted hand: 3 of Spades Queen of Clubs
Choose action: [h]it, [s]tand, [f]orfeit: h
You drew 5 of Clubs.
You: Queen of Clubs 3 of Spades 5 of Clubs (total: 18)
Sorted hand: 3 of Spades 5 of Clubs Queen of Clubs
Choose action: [h]it, [s]tand, [f]orfeit: s
-- Dealer's turn --
Dealer: 10 of Spades 7 of Diamonds (total: 17)
Dealer: 10 of Spades 7 of Diamonds (total: 17)
Dealer stands.
You win.
Play again? [y]/n: 
```

## Features implemented
- Card/Deck/Player classes with hand management, search helpers, and blackjack scoring.
- Fisher-Yates shuffle for deck randomization.
- Sorting and binary search helpers applied to gameplay (sorted hand display, blackjack detection).
- Dealer AI with standard blackjack rules; player hit/stand/forfeit loop.
- Text-based CLI that shows hands, totals, and outcomes; reshuffles shoe when low.

## Future improvements
- Add betting stack, splits, insurance, and surrender rules.
- Show running tally of player vs dealer wins.

## Libraries used
- Python standard library (`dataclasses`, `random`, `typing`).
