from .hand import Hand

class Game:
    def __init__(self, shoe):
        self.shoe = shoe
        self.player_hands = []
        self.dealer = Hand()

    def start_round(self, bet: float):
        self.player_hands = [Hand(bet)]
        self.dealer = Hand(bet=0)

        # deal initial
        for _ in range(2):
            self.player_hands[0].add(self.shoe.draw())
            self.dealer.add(self.shoe.draw())
        
        if self.player_hands[0].is_blackjack() == True:
            print("BLACKJACK")
            self.player_hands[0].is_active = False

        if self.dealer.is_blackjack() == True:
            self.player_hands[0].is_active = False

# actions: hit, stand, double, split, surrender, insurance

    def hit(self, hand: Hand):
        hand.add(self.shoe.draw())
        if hand.is_bust() == True or hand.value() == 21:
            hand.is_active = False

    def stand(self, hand: Hand):
        hand.is_active = False

    def double(self, hand: Hand):
        hand.bet *= 2
        hand.add(self.shoe.draw())
        hand.is_active = False

    def split(self, hand: Hand):
        split_hand = Hand(bet = hand.bet)
        split_hand.add(hand.cards[1])
        hand.cards.pop()
        hand.add(self.shoe.draw())
        split_hand.add(self.shoe.draw())
        self.player_hands.append(split_hand)

    def surrender(self, hand: Hand):
        hand.is_surrendered = True
        hand.is_active = False
    
    def insurance(self, hand: Hand):
        hand.is_insured = True

    # def perform_action(self, hand, action):
    #     if action == "hit":
    #         self.hit(hand)
    #     if action == "stand":
    #         self.stand(hand)
    #     if action == "double":
    #         self.double(hand)
    #     if action == "split":
    #         self.split(hand)
    #     if action == "surrender":
    #         self.surrender(hand)
    #     if action == "insurance":
    #         self.insurance(hand)

#  Dealer

    def play_dealer(self):
        while True:
            val = self.dealer.value()
            # S17 for now
            if val < 17:
                self.dealer.add(self.shoe.draw())
            else:
                break

#   Resolution

    def resolve_hand(self, hand: Hand) -> float:
        if hand.is_surrendered:
            return -0.5 * hand.bet

        if hand.is_blackjack() and not self.dealer.is_blackjack():
            return 1.5 * hand.bet

        if hand.is_bust():
            return -hand.bet

        if self.dealer.is_bust():
            return hand.bet

        pv = hand.value()
        dv = self.dealer.value()

        if pv > dv:
            return hand.bet
        elif pv < dv:
            return -hand.bet
        else:
            return 0.0

    def resolve_round(self) -> float:
        self.play_dealer()

        total = 0.0
        for hand in self.player_hands:
            total += self.resolve_hand(hand)

        return total