from cards import Cards

class Card(Cards):
    def __init__(self,suit,rank):
        Cards.__init__(self)
        self.suit = suit
        self.rank = rank
        self.value = self.values[rank]   
    def __str__(self):
        return f"{self.rank} of {self.suit}" 