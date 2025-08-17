import random



suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':[1, 11]}


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    

class Deck:

    def __init__(self):
        self.cards_on_deck = [Card(suit, rank) for suit in suits for rank in ranks]
    
    # Sheffle the deck
    def shuffle(self):
        random.shuffle(self.cards_on_deck)
    
    # Deal a card from the deck
    def deal_card(self):
       return self.cards_on_deck.pop()
        


class Player:

    def __init__(self, name: str, funds: float = 100):
        self.name = name
        self.funds = funds
        self.hand = []

    # Method to add a card to the player's hand
    def add_card(self, card: Card):
        self.hand.append(card)


    # Method to calculate the value of the hand
    def hand_value(self):
        value_without_aces = 0
        aces = 0

        # Calculate value of the hand except for aces
        for card in self.hand:
            if card.rank != 'Ace':
                value_without_aces += card.value
            else:
                aces += 1


        # Calculate the best value considering aces
        best_value = value_without_aces + aces # Consider all aces as 1 initially
        # Keep considering aces as 1's from 0 cards all the way to total aces-1
        for count_as_1 in range(aces):
            current_value = value_without_aces + (count_as_1 * 1) + (aces - count_as_1) * 11
            # Consider if you got the close to 21 or equal to 21 than the previous best 
            if current_value <= 21 and current_value > best_value:
                best_value = current_value
        
        return best_value

    def show_hand(self):
        hand_str = ', '.join(str(card) for card in self.hand)
        return f"{self.name}'s hand: {hand_str} (Value: {self.hand_value()})"

    # Method to let player pick their bet
    def place_bet(self):
        bet_amount = float(input(f"{self.name}, you have {self.funds} funds. How much would you like to bet?"))
        if bet_amount > self.funds:
            print("You cannot bet more than you have. Please try again.")
            return self.place_bet()
        else:
            self.funds -= bet_amount
            return bet_amount



class Dealer(Player):
    def __init__(self, name: str):
        self.name = name
        self.hand = []
    
    def place_bet(self):
        # Dealer does not place bets
        raise NotImplementedError("Dealer does not place bets.")
    





if __name__ == "__main__":

    # Set up the game
    print("Welcome to the Blackjack Game!")
    
    # Take the player's name and starting funds
    player_name = input("Enter your name: ")
    funds = float(input("Enter your starting funds: "))

    # Create player and dealer instances
    player = Player(player_name, funds)
    dealer = Dealer("Dealer")

    game_on = True
    
    # Main game loop
    while game_on:

        # Create a deck and shuffle it
        deck = Deck()
        deck.shuffle()

        # Player places a bet
        player_bet = player.place_bet()

        print(f"{player.name} has placed a bet of {player_bet}. Funds left: {player.funds}")

        # Deal initial cards
        for _ in range(2):
            player.add_card(deck.deal_card())
            dealer.add_card(deck.deal_card())
        
        # Show initial hands
        print(player.show_hand())
        print(f"{dealer.name}'s hand: {dealer.hand[0]}, Hidden Card")

        player_lost = False
        dealer_lost = False

        # Player's turn
        while True:
            # Check if player has busted
            if player.hand_value() > 21:
                player_lost = True
                break

            # See if player wants to hit or stand
            action = input("Do you want to (H)it or (S)tand?").strip().upper()

            # Check for invalid input
            if action != 'H' and action != 'S':
                print("Invalid Input")
                continue
            
            # If player wants to hit
            if action == 'H':
                player.add_card(deck.deal_card())
                print(player.show_hand())
            
            # If player wants to stand
            if action == 'S': break
        
        # Dealer's turn
        while not player_lost:
            # Dealer reveals his entire hand
            print(dealer.show_hand())

            # Dealer hits as long as he does not bust and has hand value less than player's
            while dealer.hand_value() < 21 and dealer.hand_value() <= player.hand_value():
                dealer.add_card(deck.deal_card())
                print(dealer.show_hand())
            
            # Check if dealer has busted
            if dealer.hand_value() > 21:
                dealer_lost = True
            # If the dealer's not busted but chose to stand then obiously player lost    
            elif dealer.hand_value() > player.hand_value():
                player_lost = True

            break
        
        # Determine the winner
        if player_lost:
            # Chekc if player busted or lost to dealer's hand
            if player.hand_value() > 21:
                print(f"{player.name} busted! Dealer wins.")
            else:
                print(f"{player.name} lost to the dealer's hand. Dealer wins")
            # # Update the player's funds    
            # player.funds -= player_bet
            print(f"{player.name} lost {player_bet}. Funds left: {player.funds}")
        elif dealer_lost:
            # Check if dealer busted
            print(f"{dealer.name} busted! {player.name} wins.")
            # Update the player's funds
            player.funds += 2 * player_bet
            print(f"{player.name} won {2 * player_bet}. Funds left: {player.funds}")
        else:
            # Both player and dealer are at 21, it's a tie
            player.funds += player_bet  # Player gets back the bet
            print(f"It's a tie! {player.name} gets back the bet of {player_bet}. Funds left: {player.funds}")

         # If player has no funds left, end the game
        if player.funds <= 0:
            print("You have no funds left. Game over!")
            break

        # Ask if the player wants to play again
        while True:
            play_again = input("Do you want to play again? (Y/N): ").strip().upper()
            if play_again not in ('Y', 'N'):
                print("Invalid input. Please enter 'Y' or 'N'.")
            else:
                game_on = True if play_again == 'Y' else False
                break
        
        # Reset hands for the next game
        player.hand = []
        dealer.hand = []

        if game_on:
            print("Starting a new game...\n")
        
    print("Thank you for playing! Goodbye!")
    


       
                 
        
            





            






    








    



