from blackjack.engine.game import Game
from blackjack.engine.hand import Hand
from blackjack.engine.shoe import Shoe

def rigged_game(cards) -> Game:
    shoe = Shoe(n_decks=1)
    shoe.cards = cards
    return Game(shoe)

def test_start_round():
    game = rigged_game([10,3,10,5])
    game.start_round(1.0)
    assert game.player_hands[0].cards == [10,10]
    assert game.dealer.cards == [3, 5]