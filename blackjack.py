from __future__ import annotations
from dataclasses import dataclass
import random
from typing import List, Optional, Tuple


RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["S", "H", "D", "C"]
RANK_ORDER = {rank: idx for idx, rank in enumerate(RANKS)}


@dataclass(frozen=True)
class Card:
    suit: str
    rank: str

    rank_names = {
        "J": "Jack",
        "Q": "Queen",
        "K": "King",
        "A": "Ace",
    }
    suit_names = {"S": "Spades", "H": "Hearts", "D": "Diamonds", "C": "Clubs"}

    @property
    def value(self) -> int:
        if self.rank in {"J", "Q", "K"}:
            return 10
        if self.rank == "A":
            return 11
        return int(self.rank)

    def __str__(self) -> str:
        rank_name = self.rank_names.get(self.rank, self.rank)
        suit_name = self.suit_names.get(self.suit, self.suit)
        return f"{rank_name} of {suit_name}"


class Deck:
    suits = SUITS
    ranks = RANKS

    def __init__(self) -> None:
        self.cards: List[Card] = []
        self.reset()

    def reset(self) -> None:
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        self.fisher_yates_shuffle()

    def fisher_yates_shuffle(self) -> None:
        for i in range(len(self.cards) - 1, 0, -1):
            j = random.randint(0, i)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def draw(self) -> Card:
        if not self.cards:
            raise RuntimeError("The deck is empty. Reset before drawing.")
        return self.cards.pop()

    def needs_shuffle(self, threshold: int = 15) -> bool:
        return len(self.cards) < threshold

    def __len__(self) -> int:
        return len(self.cards)


def insertion_sort(cards: List[Card]) -> List[Card]:
    # Stable sort helper to order cards by rank for searches and display.
    arr = cards[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and RANK_ORDER[arr[j].rank] > RANK_ORDER[key.rank]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def binary_search_by_rank(sorted_cards: List[Card], rank: str) -> Optional[int]:
    # Find the index of a rank within an already-sorted hand.
    low, high = 0, len(sorted_cards) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_cards[mid].rank == rank:
            return mid
        if RANK_ORDER[sorted_cards[mid].rank] < RANK_ORDER[rank]:
            low = mid + 1
        else:
            high = mid - 1
    return None


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.hand: List[Card] = []
        self.has_doubled = False

    def clear(self) -> None:
        self.hand.clear()
        self.has_doubled = False

    def add_card(self, card: Card) -> None:
        self.hand.append(card)

    def sorted_hand(self) -> List[Card]:
        return insertion_sort(self.hand)

    def has_rank(self, rank: str) -> bool:
        return binary_search_by_rank(self.sorted_hand(), rank) is not None

    def hand_value(self) -> Tuple[int, bool]:
        total = 0
        aces = 0
        for card in self.hand:
            if card.rank == "A":
                aces += 1
            total += card.value
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total, aces > 0 and total <= 21

    def is_busted(self) -> bool:
        total, _ = self.hand_value()
        return total > 21

    def has_blackjack(self) -> bool:
        if len(self.hand) != 2:
            return False
        sorted_cards = self.sorted_hand()
        has_ace = binary_search_by_rank(sorted_cards, "A") is not None
        has_ten_value = any(binary_search_by_rank(sorted_cards, r) is not None for r in ("10", "J", "Q", "K"))
        total, _ = self.hand_value()
        return has_ace and has_ten_value and total == 21

    def __str__(self) -> str:
        cards = " ".join(str(c) for c in self.hand)
        total, _ = self.hand_value()
        return f"{self.name}: {cards} (total: {total})"


def deal_initial(deck: Deck, player: Player, dealer: Player) -> None:
    # Start a round with two cards each for player and dealer.
    player.clear()
    dealer.clear()
    for _ in range(2):
        player.add_card(deck.draw())
        dealer.add_card(deck.draw())


def ensure_shoe(deck: Deck) -> None:
    # Refresh the deck when it gets low to avoid running out mid-hand.
    if deck.needs_shuffle():
        deck.reset()
        print("-- Shuffling new shoe --")


def format_hand(player: Player, hide_hole: bool = False) -> str:
    # Render a hand for CLI output, with optional dealer hole card hiding.
    if hide_hole and player.hand:
        return f"{player.name}: {player.hand[0]} [hidden]"
    total, _ = player.hand_value()
    return f"{player.name}: {' '.join(str(c) for c in player.hand)} (total: {total})"


def show_sorted_hand(player: Player) -> None:
    # Display hand in rank order to showcase the search/sort helpers.
    sorted_cards = player.sorted_hand()
    print(f"Sorted hand: {' '.join(str(c) for c in sorted_cards)}")


def prompt_action() -> str:
    while True:
        choice = input("Choose action: [h]it, [s]tand, [f]orfeit: ").strip().lower()
        if choice in {"h", "hit"}:
            return "h"
        if choice in {"s", "stand"}:
            return "s"
        if choice in {"f", "forfeit"}:
            return "f"
        print("Invalid choice; try again.")


def player_turn(deck: Deck, player: Player) -> str:
    # Drive the player decision loop until stand, bust, or forfeit.
    while True:
        print(format_hand(player))
        show_sorted_hand(player)
        action = prompt_action()
        if action == "h":
            try:
                card = deck.draw()
            except RuntimeError:
                deck.reset()
                card = deck.draw()
                print("-- Shuffling new shoe --")
            player.add_card(card)
            print(f"You drew {card}.")
            if player.is_busted():
                print("You busted!")
                return "bust"
        elif action == "f":
            print("You forfeited the round.")
            return "forfeit"
        else:
            return "stand"


def dealer_turn(deck: Deck, dealer: Player) -> None:
    # Dealer hits to 17, hitting on soft 17, and reveals each draw.
    print(format_hand(dealer))
    while True:
        total, has_soft_ace = dealer.hand_value()
        if total < 17 or (total == 17 and has_soft_ace):
            try:
                card = deck.draw()
            except RuntimeError:
                deck.reset()
                card = deck.draw()
                print("-- Shuffling new shoe for dealer --")
            dealer.add_card(card)
            total, _ = dealer.hand_value()
            print(f"Dealer draws {card} -> total {total}")
            if dealer.is_busted():
                print("Dealer busts!")
                return
        else:
            print("Dealer stands.")
            return


def determine_outcome(player: Player, dealer: Player) -> str:
    # Compare end-state totals and blackjack/bust conditions for result text.
    player_total, _ = player.hand_value()
    dealer_total, _ = dealer.hand_value()

    if player.is_busted():
        return "You lose (bust)."
    if dealer.is_busted():
        return "You win (dealer bust)."
    if player.has_blackjack() and not dealer.has_blackjack():
        return "Blackjack! You win."
    if dealer.has_blackjack() and not player.has_blackjack():
        return "Dealer blackjack. You lose."
    if player_total > dealer_total:
        return "You win."
    if player_total < dealer_total:
        return "You lose."
    return "Push (tie)."


def play_blackjack_cli() -> None:
    # Main game loop: deal, run player/dealer turns, show outcome, repeat.
    deck = Deck()
    player = Player("You")
    dealer = Player("Dealer")

    while True:
        ensure_shoe(deck)

        deal_initial(deck, player, dealer)
        print(format_hand(dealer, hide_hole=True))
        print(format_hand(player))

        if player.has_blackjack():
            print("Natural blackjack! Revealing dealer...")
            print(format_hand(dealer))
            print(determine_outcome(player, dealer))
        else:
            result = player_turn(deck, player)
            if result == "forfeit":
                print("Round ended by forfeit. Dealer wins.")
            elif result == "bust":
                print("Dealer wins this round.")
            else:
                print("-- Dealer's turn --")
                print(format_hand(dealer))
                dealer_turn(deck, dealer)
                print(determine_outcome(player, dealer))

        again = input("Play again? [y]/n: ").strip().lower()
        if again == "n":
            break
        print("\n--- New hand ---\n")


if __name__ == "__main__":
    play_blackjack_cli()
