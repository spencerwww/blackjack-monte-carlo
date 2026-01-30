from blackjack.engine.shoe import Shoe

def test_build_shoe():
    shoe = Shoe(n_decks=6)
    assert len(shoe.cards) == 6 * 52

def test_draw_removes_card():
    shoe = Shoe(n_decks=1)
    shoe.draw()
    assert len(shoe.cards) == 51

def test_rig_shoe():
    shoe = Shoe(n_decks=1)
    shoe.rig([5,4,9,2,0,9,7])
    assert shoe.cards[:7] == [5,4,9,2,0,9,7]