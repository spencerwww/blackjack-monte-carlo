from blackjack.engine.shoe import Shoe
from blackjack.engine.game import Game

def print_state(game):
    print("\n========================")
    print("Dealer:", game.dealer.cards[0])
    for i, hand in enumerate(game.player_hands):
        print(f"Hand {i}: {hand.cards} | value={hand.value()} | bet={hand.bet}")
    print("========================")

def print_conclusion(game, shoe):
    print("\n========================")
    print("Dealer:", game.dealer.cards, "=>", game.dealer.value())
    for i, hand in enumerate(game.player_hands):
        print(f"Hand {i}: {hand.cards} | value={hand.value()} | bet={hand.bet}")
    print("Cards left before cut: ", len(shoe.cards))
    print("========================")

def main():
    shoe = Shoe(n_decks=6)

    game = Game(shoe)

    bankroll = 1000
    bet = 10

    while True:
        game.start_round(bet)

        # if game.dealer.cards[0] == 1:
        #         print_state(game)
        #         action = input("Insurance (Y/N)").strip()

        #         if action == "Y":
        #             game.insurance(game.player_hands[0])

        #         if game.dealer.cards[1] == 10:
        #             game.player_hands[0].is_active = False

        # play all hands (including splits)

        if game.dealer.is_blackjack() == True:
            game.player_hands[0].is_active = False

        i = 0
        while i < len(game.player_hands):
            hand = game.player_hands[i]
                
            while hand.is_active:
                print_state(game)
                action = input("Action? (h / s / d / p / surrender): ").strip()

                if action == "h":
                    game.hit(hand)
                elif action == "s":
                    game.stand(hand)
                elif action == "d":
                    game.double(hand)
                elif action == "p":
                    game.split(hand)
                elif action == "surrender":
                    game.surrender(hand)
                else:
                    print("Invalid action")

            i += 1

        # dealer + settlement
        print("\n--- Dealer plays ---")
        game.play_dealer()
        print_conclusion(game, shoe)

        pnl = game.resolve_round()
        bankroll += pnl

        print("\nPNL:", pnl)
        print("Bankroll:", bankroll)


if __name__ == "__main__":
    main()
