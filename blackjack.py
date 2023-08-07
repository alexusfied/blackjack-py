import random

values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':11,'King':12,'Queen':13,'Ace':14}
suits = ('Hearts','Clubs',"Diamonds",'Spades')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','King','Queen','Ace')

# Card, Deck and Player classes are defined
class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]   
    def __str__(self):
        return f"{self.rank} of {self.suit}"    
    
class Deck: 
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)
                self.all_cards.append(created_card)      
    def shuffle(self):
        random.shuffle(self.all_cards)   
    def deal_one(self):
        return self.all_cards.pop()  
     
class Player:
    def __init__(self,name,total_money):
        self.name = name
        self.hand = []
        self.total_money = total_money    
    def hit(self,drawn_card):
        self.hand.append(drawn_card)    
    def stand(self):
        pass
    def wager(self,wager_amount):
        self.wager_amount = wager_amount
        return self.wager_amount
    def r4ise(self,r4ise_amount):
        self.r4ise_amount = r4ise_amount
        self.total_money = self.total_money - self.r4ise_amount  
    def show_hand(self):
        count = 0
        for i in self.hand:
            print(f"{self.name}: {self.hand[count]}")
            count += 1      
    def hand_value(self):
        hand_value = 0
        counter = 0 
        for i in self.hand:
            hand_value = hand_value + self.hand[counter].value
            counter += 1 
        return hand_value
    def delete_hand(self):
        self.hand = []
    def set_bank(self,current_wager):
        self.current_wager = current_wager
        self.total_money = self.total_money - self.current_wager
        return self.total_money
    def check_bank(self):
        has_money = True
        if self.total_money > 0:
            has_money = True   
        else:
            has_money = False
        return has_money  
    def win(self,win_sum):
        self.total_money = self.total_money + win_sum
        return self.total_money

# Additional functions    
def ask_name():
    player_name = input('What is your name? ')  
    return player_name

def convertibleToInt(value):
    try:
        valueInt = int(value)
        return True
    except:
        return False
    
def ask_money():
    player_money = input("How much money do you want to put in your bank? ")
    if (convertibleToInt(player_money)):
        return int(player_money)
    while type(player_money) != int:
        player_money = input("That's not a number. How much do you want to put in your bank? ")
        if (convertibleToInt(player_money)):
            player_money = int(player_money)    
    return player_money

def ask_raise():
    r4ise = int(input("By how much do you want to raise? "))
    if (convertibleToInt(r4ise)):
        return int(r4ise)
    while type(r4ise != int):
        r4ise = input("That's not a number. How much do you want to raise? ")
        if (convertibleToInt(r4ise)):
            r4ise = int(r4ise)    
    return r4ise

def ask_wager():    
    wager = input("How much do you want to wager? ")
    if (convertibleToInt(wager)):
        return int(wager)
    while type(wager) != int:
        wager = input("That's not a number. How much do you want to wager? ")
        if (convertibleToInt(wager)):
            wager = int(wager)    
    return wager

def play_again():
    again = False
    user_input = input("Do you want to keep playing? ")
    possible_answers = ["Yes","No"]
    while user_input.capitalize() not in possible_answers:
        user_input = input("Sorry, didn't understand. Do you want to keep playing? ") 
    if user_input.capitalize() == "Yes":
        again = True  
    else:
        again = False  
    return again

# Main -> Game logic
if (__name__ == "__main__"):
    dealer = Player('Dealer',100000000)
    Player_1 = Player(ask_name(),ask_money())


    while True:
        game_on = True
        turn = "Player 1"
        player1_stand = False
        dealer_stand = False
        Game_Deck = Deck()
        Game_Deck.shuffle()
        first_cards = []

        print("The game is on!")

        for i in range (2):
            first_cards.append(Game_Deck.deal_one())

        Player_1.hit(first_cards[0])
        Player_1.show_hand()
        print(f"{Player_1.name}'s current hand value is {Player_1.hand_value()}.")

        dealer.hit(first_cards[1])
        dealer.show_hand()
        print(f"Dealers current hand value is {dealer.hand_value()}.")

        print(f"{Player_1.name} has {Player_1.total_money} in his bank.")
        p1_wager = Player_1.wager(ask_wager())
        
        while p1_wager > Player_1.total_money:
            print("Sorry, you don't have enough money in your bank.")
            p1_wager = Player_1.wager(ask_wager())
            
        Player_1.set_bank(p1_wager)
        print(f"{Player_1.name} has {Player_1.total_money} in his bank.")
        
        dealer_wager = dealer.wager(p1_wager)
        
        pot = p1_wager + dealer_wager
            
            
        while game_on:

            if turn == "Player 1" and player1_stand == False:
                input_p1 = input("Do you want to hit, stand or raise? ")
                possible_answers = ["Hit","Stand","Raise"]

                while input_p1.capitalize() not in possible_answers:
                    input_p1 = input("Sorry, didn't understand. Do you want to hit, stand or raise? ")

                if input_p1.capitalize() == "Hit":
                    card = Game_Deck.deal_one()
                    Player_1.hit(card)
                    Player_1.show_hand()
                    p1_hand_value = Player_1.hand_value()
                    print(f"Current hand value is {p1_hand_value}.")

                    if p1_hand_value < 21:
                        pass

                    elif p1_hand_value == 21:
                        print(f"Winner winner, chicken dinner. {Player_1.name} wins!")
                        Player_1.win(pot)
                        money_left = Player_1.check_bank()
                        break

                    else:
                        print(f"{Player_1.name} loses.")
                        dealer.win(pot)
                        money_left = Player_1.check_bank()
                        break

                    turn = "Dealer"

                elif input_p1.capitalize() == "Stand":
                    Player_1.stand()
                    Player_1.show_hand()
                    turn = "Dealer"
                    player1_stand = True

                elif input_p1.capitalize() == "Raise":
                    p_raise = ask_raise()
                    
                    while p_raise > Player_1.total_money:
                        print(f"You don't have enough money in your bank account. Current balance is {Player_1.total_money}.")
                        if Player_1.total_money == 0:
                            print("Type in 0 to continue.")
                        p_raise = ask_raise()
                        
                    Player_1.r4ise(p_raise)

            else:
                turn = "Dealer"

            if turn == "Dealer" and dealer_stand == False:
                dealer_hand_value = dealer.hand_value()
                p1_hand_value = Player_1.hand_value()

                if dealer_hand_value < 17:
                    card = Game_Deck.deal_one()
                    dealer.hit(card)
                    dealer.show_hand()
                    dealer_hand_value = dealer.hand_value()
                    print(f"Current hand value is {dealer_hand_value}.")

                else:
                    dealer.stand()
                    dealer_stand = True

                if dealer_hand_value < 21:
                    pass

                elif dealer_hand_value == 21:
                    print("House wins!")
                    dealer.win(pot)
                    money_left = Player_1.check_bank()
                    break

                else:
                    print("House loses.")
                    Player_1.win(pot)
                    money_left = Player_1.check_bank()
                    break


                turn = "Player 1"

            if player1_stand == True and dealer_stand == True:

                if p1_hand_value > dealer_hand_value:
                    print(f"{Player_1.name} wins!")
                    money_left = Player_1.check_bank()
                    Player_1.win(pot)
                    break

                elif p1_hand_value == dealer_hand_value:
                    print("It's a tie.")
                    Player_1.win(p1_wager)
                    money_left = Player_1.check_bank()
                    dealer.win(dealer_wager)
                    break

                else:
                    print("House wins!")
                    dealer.win(pot)
                    money_left = Player_1.check_bank()
                    break

            else:
                pass
        
        game_on = play_again()
        if game_on == True and money_left == True:
            Player_1.delete_hand()
            dealer.delete_hand()
        
        elif game_on == True and money_left == False:
            print("Sorry, you don't have any money left in your bank.")
            break
            
        else:
            break