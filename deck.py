from cards import Cards
from card import Card
import random

class Deck(Cards): 
    def __init__(self):
        Cards.__init__(self)
        self.all_cards = []
        for suit in self.suits:
            for rank in self.ranks:
                created_card = Card(suit,rank)
                self.all_cards.append(created_card)      
    def shuffle(self):
        random.shuffle(self.all_cards)   
    def deal_one(self):
        return self.all_cards.pop()  
   