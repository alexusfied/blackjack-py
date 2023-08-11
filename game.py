from player import Player
from deck import Deck

class Game:
    def __init__(self):
        self.player = Player(self.askName(),self.askMoney())
        self.dealer = Player("Dealer",100000000)
        self.players = [self.player, self.dealer]
        self.gameOn = False
        self.turn = ""
        self.deck = Deck()
        self.firstCards = []
        self.pot = 0

    # -------------- RESETS ALL NECESSARY PARAMETERS, SO A NEW ROUND CAN START -------------
    def prepNewRound(self):
        self.gameOn = True
        for player in self.players:
            player.stands = False
            player.delete_hand()
        self.firstCards.clear()
        self.pot = 0
        self.changeTurn("player")
        self.deck.shuffle()

    # -------------- DEALS THE FIRST CARD TO PLAYER AND DEALER, PRINTS THE HAND VALUES AND ASKS THE PLAYER FOR A WAGER -------------
    def dealFirst(self):
        for i in range (2):
            self.firstCards.append(self.deck.deal_one())
        # First cards are drawn -> each player draws one card which is then added to their hands
        self.player.hit(self.firstCards[0])
        self.player.show_hand()
        print(f"{self.player.namePoss} current hand value is {self.player.hand_value()}.\n")
        self.dealer.hit(self.firstCards[1])
        self.dealer.show_hand()
        print(f"Dealer's current hand value is {self.dealer.hand_value()}.\n")
        # Hand value of the player is printed and then the user is prompted for a wager. The user input is checked for a valid value
        print(f"{self.player.name} has {self.player.total_money} in his bank.")
        self.player.wager(self.ask_wager())
        while self.player.wager_amount > self.player.total_money:
            print("Sorry, you don't have enough money in your bank.")
            self.player.wager(self.ask_wager())
        # The player's bank is updated
        self.player.set_bank(self.player.wager_amount)
        print(f"{self.player.name} has {self.player.total_money} in his bank.")
        # The dealer sets his wager (which is always the same as the player's) and the pot is updated
        dealer_wager = self.dealer.wager(self.player.wager_amount)
        self.pot = self.player.wager_amount + dealer_wager

    # -------------- BASED ON WHO'S TURN IT IS, SIMULATES THE DEALER'S TURN OR LETS THE PLAYER CHOOSE A MOVE + DETERMINES WHETHER THE ROUND CONTINUES OR IS FINISHED -------------
    def takeTurn(self):
        roundContinues = True
        # Player's turn
        if self.turn == "player" and self.player.stands == False:
            print("-------------------------------")
            inputPlayer = input("Do you want to hit, stand or raise? ")
            possibleAnswers = ["Hit","Stand","Raise"]
            # Check for valid user input
            while inputPlayer.capitalize() not in possibleAnswers:
                inputPlayer = input("Sorry, didn't understand. Do you want to hit, stand or raise? ")
            # Check whether the player hits, stands or raises
            if inputPlayer.capitalize() == "Hit":
                print("-------------------------------")
                card = self.deck.deal_one()
                self.player.hit(card)
                self.player.show_hand()
                handValuePlayer = self.player.hand_value()
                print(f'{self.player.namePoss} hand value is {handValuePlayer}.\n')
                if handValuePlayer < 21:
                    self.changeTurn("dealer")
                elif handValuePlayer == 21:
                    print(f"Winner winner, chicken dinner. {self.player.name} wins!")
                    self.player.win(self.pot)
                    self.player.moneyLeft = self.player.check_bank()
                    roundContinues = False
                else:
                    print(f"{self.player.name} loses.")
                    self.dealer.win(self.pot)
                    self.player.moneyLeft = self.player.check_bank()
                    roundContinues = False
            elif inputPlayer.capitalize() == "Stand":
                self.player.stand()
                self.player.show_hand()
                self.changeTurn("dealer")
            elif inputPlayer.capitalize() == "Raise":
                playerRaise = self.ask_raise()
                while playerRaise > self.player.total_money:
                    print(f"You don't have enough money in your bank account. Current balance is {self.player.total_money}.")
                    if self.player.total_money == 0:
                        print("Type in 0 to continue.")
                    playerRaise = self.ask_raise()        
                self.player.r4ise(playerRaise)
                print(f"{self.player.name} has {self.player.total_money} in his bank.")
        # Dealer's turn  
        if self.turn == "dealer" and self.dealer.stands == False:
            handValueDealer = self.dealer.hand_value()
            handValuePlayer = self.player.hand_value()
            if handValueDealer < 17:
                card = self.deck.deal_one()
                self.dealer.hit(card)
                self.dealer.show_hand()
                handValueDealer = self.dealer.hand_value()
                print(f"Dealer's hand value is {handValueDealer}.\n")
            else:
                self.dealer.stand()
            if handValueDealer < 21:
                pass
            elif handValueDealer == 21:
                print("House wins!")
                self.dealer.win(self.pot)
                self.player.moneyLeft = self.player.check_bank()
                roundContinues = False
            else:
                print("House loses.")
                self.player.win(self.pot)
                self.player.moneyLeft = self.player.check_bank()
                roundContinues = False
            self.changeTurn("player")
        # If both dealer and player stand, winner is calculated based on the hand values
        if self.player.stands == True and self.dealer.stands == True:
            if handValuePlayer > handValueDealer:
                print(f"{self.player.name} wins!")
                self.player.money_left = self.player.check_bank()
                self.player.win(self.pot)
                roundContinues = False
            elif handValuePlayer == handValueDealer:
                print("It's a tie.")
                self.player.win(self.player.wager_amount)
                self.player.moneyLeft = self.player.check_bank()
                self.dealer.win(self.dealer.wager_amount)
                roundContinues = False
            else:
                print("House wins!")
                self.dealer.win(self.pot)
                self.player.moneyLeft = self.player.check_bank()
                roundContinues = False
        else:
            pass
        return roundContinues
    
    # -------------- CHANGES THE TURN -------------
    def changeTurn(self, player):
        self.turn = player

    # -------------- ASKS THE PLAYER FOR A NAME -------------
    def askName(self):
        playerName = input("What is your name? ")
        return playerName
    
    # -------------- ASKS THE PLAYER HOW MUCH MONEY SHOULD BE PUT IN THE BANK -------------
    def askMoney(self):
        print("-------------------------------")
        playerMoney = input("How much money do you want to put in your bank? ")
        if (self.convertibleToInt(playerMoney)):
            return int(playerMoney)
        while type(playerMoney) != int:
            playerMoney = input("That's not a number. How much do you want to put in your bank? ")
            if (self.convertibleToInt(playerMoney)):
                playerMoney = int(playerMoney) 
        return playerMoney
    
    # -------------- ASKS THE PLAYER BY HOW MUCH THE WAGER SHOULD BE RAISED -------------
    def ask_raise(self):
        print("-------------------------------")
        r4ise = int(input("By how much do you want to raise? "))
        if (self.convertibleToInt(r4ise)):
            return int(r4ise)
        while type(r4ise != int):
            r4ise = input("That's not a number. How much do you want to raise? ")
            if (self.convertibleToInt(r4ise)):
                r4ise = int(r4ise)    
        return r4ise
    
    # -------------- ASKS THE PLAYER FOR A WAGER-------------
    def ask_wager(self):
        print("-------------------------------")    
        wager = input("How much do you want to wager? ")
        if (self.convertibleToInt(wager)):
            return int(wager)
        while type(wager) != int:
            wager = input("That's not a number. How much do you want to wager? ")
            if (self.convertibleToInt(wager)):
                wager = int(wager)    
        return wager
    
    # -------------- ASKS THE PLAYER IF THE GAME SHOULD BE CONTINUED. CONTINUING IS ONLY POSSIBLE IF THERE IS MONEY LEFT IN THE BANK -------------
    def play_again(self):
        again = False
        print("-------------------------------")
        user_input = input("Do you want to keep playing [yes|no]? ")
        possible_answers = ["Yes","No"]
        while user_input.capitalize() not in possible_answers:
            user_input = input("Sorry, didn't understand. Do you want to keep playing? ") 
        if user_input.capitalize() == "Yes" and self.player.moneyLeft > 0:
            again = True
        elif user_input.capitalize() == "Yes" and self.player.moneyLeft == 0:
            print("Sorry, you don't have any money left.")
            again = False  
        else:
            again = False  
        return again
    
    # -------------- HELPER METHOD TO CHECK IF AN INPUT IS CONVERTIBLE TO INT -------------
    def convertibleToInt(self, value):
        try:
            valueInt = int(value)
            return True
        except:
            return False  