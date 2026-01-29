BLACKJACK = 21

class Hand:
    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def value(self):
        total = sum(self.cards)
        has_ace = 1 in self.cards

        if len(self.cards) == 2 and total == 11 and has_ace:
            return 21  # natural blackjack

        if has_ace and total + 10 <= 21:
            return total + 10

        return total

    def is_blackjack(self):
        return len(self.cards) == 2 and self.value() == 21

    def is_bust(self):
        return self.value() > 21