from typing import Type

from card import Card


class SolitaireStack:

    def __init__(self):
        self.faceUpStack = []
        self.faceDownStack = []

    def addFaceUpCard(self, card: Card):
        self.faceUpStack.append(card)

    def addFaceDownCard(self, card: Card):
        self.faceDownStack.append(card)

    def addFaceUpCardStack(self, cards):
        if type(cards) != type([Card]):
            raise TypeError(
                "SolitaireStack.addFaceUpCardStack requires a [Card] argument, not "
                + str(type(cards))
            )
        self.faceUpStack += cards

    def revealTopFaceDownCard(self):
        if self.faceDownStack:
            self.faceUpStack.append(self.faceDownStack.pop())

    def removeTopCard(self, revealTop=True):
        if self.faceUpStack:
            oldTopCard = self.faceUpStack.pop()
        else:
            return None
        if not self.faceUpStack and revealTop:
            self.revealTopFaceDownCard()
        return oldTopCard

    def removeFaceUpStack(self):
        oldStack = self.faceUpStack.copy()
        self.faceUpStack.clear()
        self.revealTopFaceDownCard()
        return oldStack

    def __str__(self):
        string = ""
        for i in range(len(self.faceDownStack)):
            string += "??? | "
        for card in self.faceUpStack:
            string += str(card)
            string += " | "
        string = string[:-2]
        return string

    def highFaceUpCard(self):
        if self.faceUpStack:
            return self.faceUpStack[0]
        else:
            return None

    def lowFaceUpCard(self):
        if self.faceUpStack:
            return self.faceUpStack[-1]
        else:
            return None

    def getFaceDownStackSize(self):
        return len(self.faceDownStack)

    def getFaceUpStackSize(self):
        return len(self.faceUpStack)
