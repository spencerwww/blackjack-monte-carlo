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
    game = rigged_game([8,5,8,3,10,7])
    game.start_round(1.0)
    hand = game.player_hands[0]
    game.split(hand)
    assert game.player_hands[0].cards == [8, 10]
    assert game.player_hands[1].cards == [8, 7]

def test_split_not_allowed():
    game = rigged_game([4,5,3,3])
    game.start_round(1.0)
    hand = game.player_hands[0]
    with pytest.raises(ValueError):
        game.split(hand)

def test_resplit():
    game = rigged_game([8,5,8,4,8,3,1,2])
    game.start_round(1.0)
    hand = game.player_hands[0]
    game.split(hand)
    game.split(hand)
    assert game.player_hands[0].cards == [8, 1]
    assert game.player_hands[1].cards == [8, 2]
    assert game.player_hands[2].cards == [8, 3]

def test_surrender_after_action():
    game = rigged_game([5,10,3,10,8])
    game.start_round(1.0)
    hand = game.player_hands[0]
    game.hit(hand)
    with pytest.raises(ValueError):
        game.surrender(hand)

def test_insurance_not_offered():
    game = rigged_game([8,10,3,1])
    game.start_round(1.0)
    hand = game.player_hands[0]
    with pytest.raises(ValueError):
        game.insurance(hand)

def test_action_after_inactive():
    game = rigged_game([10,2,2,10,10,7])
    game.start_round(1.0)
    hand = game.player_hands[0]
    game.hit(hand)
    with pytest.raises(ValueError):
        game.hit(hand)
    with pytest.raises(ValueError):
        game.stand(hand)
    with pytest.raises(ValueError):
        game.double(hand)

def test_play_dealer_stand_seventeen():
    game = rigged_game([10,5,7,6,6,4])
    game.start_round(1.0)
    hand = game.player_hands[0]
    game.stand(hand)
    game.play_dealer()
    assert game.dealer.cards == [5,6,6]

def test_play_dealer_draw_to_sixteen():
    game = rigged_game([10,5,7,6,5,2,3])
    game.start_round(1.0)
    hand = game.player_hands[0]
    game.stand(hand)
    game.play_dealer()
    assert game.dealer.cards == [5,6,5,2]

def test_resolve_hand_player_win():
    game = rigged_game([10,7,10,10])
    game.start_round(1.0)
    hand = game.player_hands[0]
    game.stand(hand)
    game.play_dealer()
    pnl = game.resolve_hand(hand)
    assert pnl == 1.0

def test_resolve_hand_player_loss():
    game = rigged_game([10,10,7,10])
    game.start_round(1.0)
    hand = game.player_hands[0]
    game.stand(hand)
    game.play_dealer()
    pnl = game.resolve_hand(hand)
    assert pnl == -1.0

def test_resolve_hand_player_blackjack():
    game = rigged_game([10,10,1,10])
    game.start_round(1.0)
    hand = game.player_hands[0]
    game.play_dealer()
    pnl = game.resolve_hand(hand)
    assert pnl == 1.5

def test_resolve_hand_both_blackjack():
    game = rigged_game([10,10,1,1])
    game.start_round(1.0)
    hand = game.player_hands[0]
    game.play_dealer()
    pnl = game.resolve_hand(hand)
    assert pnl == 0.0

def test_resolve_hand_player_bust():
    game = rigged_game([10,2,2,10,10,5])
    game.start_round(1.0)
    hand = game.player_hands[0]
    game.hit(hand)
    game.play_dealer()
    pnl = game.resolve_hand(hand)
    assert pnl == -1.0

def test_resolve_hand_dealer_bust():
    game = rigged_game([10,2,7,10,10])
    game.start_round(1.0)
    hand = game.player_hands[0]
    game.stand(hand)
    game.play_dealer()
    print(hand.cards)
    print(game.dealer.cards)
    pnl = game.resolve_hand(hand)
    assert pnl == 1.0

def test_resolve_hand_surrender():
    game = rigged_game([10,10,6,10])
    game.start_round(1.0)
    hand = game.player_hands[0]
    game.surrender(hand)
    game.play_dealer()
    pnl = game.resolve_hand(hand)
    assert pnl == -0.5

def test_resolve_hand_insurance_blackjack():
    game = rigged_game([10,1,6,10])
    game.start_round(1.0)
    hand = game.player_hands[0]
    game.insurance(hand)
    game.play_dealer()
    pnl = game.resolve_hand(hand)
    assert pnl == 0.0

def test_resolve_hand_insurance_no_blackjack():
    game = rigged_game([10,1,6,9])
    game.start_round(1.0)
    hand = game.player_hands[0]
    game.insurance(hand)
    game.play_dealer()
    pnl = game.resolve_hand(hand)
    assert pnl == -1.5

def test_resolve_hand_insurance_player_bj_dealer_no_bj():
    game = rigged_game([10,1,1,9])
    game.start_round(1.0)
    hand = game.player_hands[0]
    game.insurance(hand)
    game.play_dealer()
    pnl = game.resolve_hand(hand)
    assert pnl == 1.0

def test_resolve_hand_insurance_both_blackjack():
    game = rigged_game([10,1,1,10])
    game.start_round(1.0)
    hand = game.player_hands[0]
    game.insurance(hand)
    game.play_dealer()
    pnl = game.resolve_hand(hand)
    assert pnl == 1.0

def test_resolve_round():
    game = rigged_game([8,10,8,7,10,10])
    game.start_round(1.0)
    game.split(game.player_hands[0])
    game.stand(game.player_hands[0])
    game.stand(game.player_hands[1])
    game.play_dealer()
    assert game.resolve_round() == 2.0