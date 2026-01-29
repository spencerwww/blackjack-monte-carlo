from .hand import Hand

class Game:
    def __init__(self, shoe):
        self.shoe = shoe
        self.player = Hand()
        self.dealer = Hand()

    def deal_initial(self):
        self.player.add(self.shoe.draw())
        self.dealer.add(self.shoe.draw())
        self.player.add(self.shoe.draw())
        self.dealer.add(self.shoe.draw())