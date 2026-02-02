from blackjack.engine.game import Game
from blackjack.engine.hand import Hand
from blackjack.engine.shoe import Shoe
import pytest

def rigged_game(cards) -> Game:
    shoe = Shoe(n_decks=1)
    shoe.cards = cards
    return Game(shoe)

def test_start_round():
    game = rigged_game([10,3,10,5])
    game.start_round(1.0)
    assert game.player_hands[0].cards == [10,10]
    assert game.dealer.cards == [3, 5]

def test_check_immediate_round_end_player_bj():
    game = rigged_game([10,6,1,7])
    game.start_round(1.0)
    game2 = rigged_game([1,6,10,7])
    game2.start_round(1.0)
    assert game.check_immediate_round_end() == True
    assert game2.check_immediate_round_end() == True

def test_check_immediate_round_end_dealer_bj():
    game = rigged_game([10,10,7,1])
    game.start_round(1.0)
    assert game.check_immediate_round_end() == True

def test_hit():
    game = rigged_game([5,10,3,3,10])
    game.start_round(1.0)
    hand = game.player_hands[0]
    game.hit(hand)
    assert hand.cards == [5,3,10]
    assert hand.is_active == True

def test_stand():
    game = rigged_game([5,10,3,3,10])
    game.start_round(1.0)
    hand = game.player_hands[0]
    game.stand(hand)
    assert hand.cards == [5,3]
    assert hand.is_active == False

def test_double():
    game = rigged_game([5,8,6,3,10])
    game.start_round(1.0)
    hand = game.player_hands[0]
    game.double(hand)
    assert hand.bet == 2.0
    assert hand.cards == [5,6,10]
    assert hand.is_active == False

def test_double_after_hit():
    game = rigged_game([4,5,3,6,4,10])
    game.start_round(1.0)
    hand = game.player_hands[0]
    game.hit(hand)
    with pytest.raises(ValueError):
        game.double(hand)



def test_split():
    game = rigged_game([5,8,6,3,10])
    game.start_round(1.0)