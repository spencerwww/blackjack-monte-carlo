from blackjack.engine.hand import Hand

def test_add_card():
    h = Hand()
    h.add(7)
    h.add(10)
    assert h.cards == [7,10]

def test_hard_value():
    h = Hand()
    h.cards = [7, 10]
    assert h.value() == 17

def test_soft_value():
    h = Hand()
    h.cards = [6, 1]
    assert h.value() == 17

def test_many_cards_no_ace():
    h = Hand()
    h.cards = [2,2,3,5,4,3,2]
    assert h.value() == 21

def test_many_aces_soft():
    h = Hand()
    h.cards = [1,1,1]
    assert h.value() == 13

def test_many_aces_hard():
    h = Hand()
    h.cards = [10,1,1,1]
    assert h.value() == 13

def test_blackjack_true():
    h1 = Hand()
    h1.cards = [1,10]
    h2 = Hand()
    h2.cards = [10,1]
    h3 = Hand()
    assert h1.is_blackjack() == True
    assert h2.is_blackjack() == True

def test_blackjack_false():
    h1 = Hand()
    h1.cards = [1,5,5]
    h2 = Hand()
    h2.cards = [10,5,6]
    assert h1.is_blackjack() == False
    assert h2.is_blackjack() == False

def test_is_bust_true():
    h1 = Hand()
    h1.cards = [10,5,7]
    h2 = Hand()
    h2.cards = [9,1,10,3]
    assert h1.is_bust() == True
    assert h2.is_bust() == True

def test_is_bust_false():
    h1 = Hand()
    h1.cards = [10,9]
    h2 = Hand()
    h2.cards = [1,1,10,5]
    assert h1.is_bust() == False
    assert h2.is_bust() == False


