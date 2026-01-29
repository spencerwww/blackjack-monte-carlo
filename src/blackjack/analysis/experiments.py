from blackjack.engine.shoe import Shoe
from blackjack.engine.game import Game

shoe = Shoe(n_decks=6)

game = Game(shoe)
game.deal_initial()

print("Dealer upcard:", game.dealer.cards[0])
print("Player hand:", game.player.cards)
print("Player value:", game.player.value())