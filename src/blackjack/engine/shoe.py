import random

class Shoe:
    def __init__(self, n_decks, lower_cut=0.75, upper_cut=1.5):
        self.n_decks = n_decks
        self.lower_cut = lower_cut
        self.upper_cut = upper_cut
        self.cards = self._build_shoe()
        # self._cut()

    def _build_shoe(self):
        ranks = [1,2,3,4,5,6,7,8,9,10,10,10,10]
        shoe = ranks * 4 * self.n_decks
        random.shuffle(shoe)
        return shoe

    def _cut(self):
        deck_len = 52
        cut = random.randint(
            int(self.lower_cut * deck_len),
            int(self.upper_cut * deck_len)
        )
        self.cards = self.cards[:-cut]

    def draw(self):
        return self.cards.pop(0)
    
    def rig(self, rig_cards):
        self.cards = rig_cards + self.cards
