from blackjack.engine.shoe import Shoe
from blackjack.engine.game import Game
import time

def print_state(game: Game, conclusion: bool):
    print("\n========================")
    if conclusion:
        print("Dealer:", game.dealer.cards, "=>", game.dealer.value())
    else:
        print("Dealer:", game.dealer.cards[0])
    for i, hand in enumerate(game.player_hands):
        print(f"Hand {i}: {hand.cards} | value={hand.value()} | bet={hand.bet}")
    print("========================")

def conclude_round(game: Game):
    print_state(game, True)

    pnl = game.resolve_round()

    print("\nPNL:", pnl)

def check_immediate_round_end(game: Game) -> bool:
    # check for player blackjack
    if (game.player_hands[0].is_blackjack()):
        return False
    
    # check for dealer blackjack (upcard is 10)
    if game.dealer.cards[0] == 10 and game.dealer.is_blackjack():
        return False
    
    return True
    
def main():
    shoe = Shoe(n_decks=6)
    # shoe.rig([1,10,10,1])

    game = Game(shoe)

    bankroll: float = 1000

    print("----------- BLACKJACK -----------")
    print("BLACKJACK PAYS 3 TO 2")
    print("DEALER MUST DRAW TO 16, STAND ON ALL 17S")
    print("INSURANCE PAYS 1 TO 1")

    while True:
        if bankroll <= 0:
            print("----------- BANKRUPT -----------")
            break

        try:
            bet = float(input("Place your bet (Min bet 10): ").strip())
        except ValueError:
            print("Bet must be a valid number")
            continue
        if bet < 10:
            print("Minimum bet is 10")
            continue
        if bet > bankroll:
            print("Bet larger than remaining bankroll")
            continue


        game.start_round(bet)

        # game.player_hands[0].is_active = check_immediate_round_end(game)

        # if dealer upcard is ace, offer insurance
        if game.dealer.cards[0] == 1:
            print_state(game, False)
            action = input("Insurance (y to accept): ").strip()

            if action == "y":
                game.player_hands[0].is_insured = True
                print("Insurance accepted")
            else:
                print("Insurance denied")

            if game.dealer.is_blackjack():
                game.player_hands[0].is_active = False

        # play all hands (including splits)

        i = 0
        while i < len(game.player_hands):
            hand = game.player_hands[i]
                
            while hand.is_active:
                print_state(game, False)
                print("Hit: h")
                print("Stand: s")
                if len(hand.cards) == 2:
                    print ("Double: d")
                if len(hand.cards) == 2 and hand.cards[0] == hand.cards[1]:
                    print("Split: p")
                if len(hand.cards) == 2 and not hand.is_split:
                    print("Surrender: sur")

                action = input("Action: ").strip()

                if action == "h":
                    game.hit(hand)
                elif action == "s":
                    game.stand(hand)
                elif action == "d":
                    if (bet > 0.5 * bankroll):
                        print("Not enough money to double")
                    else:
                        game.double(hand)
                elif action == "p":
                    game.split(hand)
                elif action == "sur":
                    game.surrender(hand)
                else:
                    print("Invalid action")

            i += 1

        # dealer + settlement
        print("\n--- Dealer plays ---")
        game.play_dealer()
        print_state(game,True)
        pnl = game.resolve_round()
        bankroll += pnl
        print("PnL: ", pnl)
        print("Bankroll: ", bankroll)
        input("Press any key to continue").strip()
        


if __name__ == "__main__":
    main()
