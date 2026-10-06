class Card:
    suit = ""
    rank = 0
    color = ""

    def __init__(self, s="", r=0):
        self.suit = s
        self.rank = r
        if self.suit == "S" or self.suit == "C":
            self.color = "b"
        elif self.suit == "H" or self.suit == "D":
            self.color = "R"

    def getSuit(self):
        return self.suit

    def getRank(self):
        return self.rank

    def getColor(self):
        return self.color

    def setSuit(self, s=""):
        self.suit = s
        if self.suit == "S" or self.suit == "C":
            self.color = "b"
        elif self.suit == "H" or self.suit == "D":
            self.color = "R"

    def setRank(self, r=0):
        self.rank = r

    def __str__(self):

        if self.rank == 11:
            return "J of " + self.suit
        elif self.rank == 12:
            return "Q of " + self.suit
        elif self.rank == 13:
            return "K of " + self.suit
        elif self.rank == 1:
            return "A of " + self.suit
        else:
            return str(self.rank) + " of " + self.suit
