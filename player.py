class Player:
    def __init__(self,name,total_money):
        self.name = name
        self.namePoss = self.name + "'s" if self.name[-1] != "s" else self.name + "'"
        self.hand = []
        self.total_money = total_money
        self.moneyLeft = total_money
        self.stands = False
    def hit(self,drawn_card):
        print(f"{self.name} has drawn {drawn_card}")
        print("")
        self.hand.append(drawn_card)    
    def stand(self):
        self.stands = True
        pass
    def wager(self,wager_amount):
        self.wager_amount = wager_amount
        return self.wager_amount
    def r4ise(self,r4ise_amount):
        self.r4ise_amount = r4ise_amount
        self.total_money = self.total_money - self.r4ise_amount  
    def show_hand(self):
        count = 0
        print(f"{self.namePoss} hand:")
        for i in self.hand:
            print(f"{self.hand[count]}")
            count += 1 
        print("\n")     
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