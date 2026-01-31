BLACKJACK = 21

class Hand:
    def __init__(self, bet=1.0):
        self.cards = []
        if bet <= 0:
            raise Exception("Bet must be greater than zero")
        self.bet = bet
        self.is_active = True
        self.is_surrendered = False
        self.is_insured = False

    def add(self, card: int):
        self.cards.append(card)

    def value(self) -> int:
        total = sum(self.cards)
        has_ace = 1 in self.cards

        if len(self.cards) == 2 and total == 11 and has_ace:
            return 21  # natural blackjack

        if has_ace and total + 10 <= 21:
            return total + 10

        return total

    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.value() == 21

    def is_bust(self) -> bool:
        return self.value() > 21