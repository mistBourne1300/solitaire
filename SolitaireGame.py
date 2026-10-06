import os
from random import shuffle

from aceStack import AceStack
from card import Card
from helperStack import helperStack
from SolitaireStack import SolitaireStack


class SolitaireGame:

    def __init__(self, deck, shuf=True):
        if type(deck) != type([Card]):
            raise TypeError(
                "SolitaireGame.__init__ requires a [Card] argument, not "
                + str(type(deck))
            )
        if len(deck) != 52:
            raise ValueError(f"Deck must be len 52, not {len(deck)}")
        self.aceStacks = []
        self.SolitaireStacks = []
        self.helpStack = helperStack()
        if shuf:
            shuffle(deck)
        # print(deck[0])
        for i in range(7):
            newSStack = SolitaireStack()
            for j in range(i + 1):
                # print("i,j:",str(i), str(j))
                newSStack.addFaceDownCard(deck.pop(0))
            newSStack.revealTopFaceDownCard()
            self.SolitaireStacks.append(newSStack)

        while deck:
            self.helpStack.addFaceDownCard(deck.pop())
        # print(self)

    def __str__(self):
        string = "Solitaire Stacks\n\n"
        for i in range(len(self.SolitaireStacks)):
            string += str(i) + ": " + str(self.SolitaireStacks[i]) + "\n"
        string += "\n\n\nHelper Stack\n\n" + str(self.helpStack)
        string += "\n\n\nAce Stacks\n\n"
        for stack in self.aceStacks:
            string += str(stack) + " | "
        string += "\n\n\n"
        return string

    def makeMove(self, choice=0, fromStack=0, toStack=0):
        TERMINATE = -1
        MOVE_ENTIRE_STACK = 0
        MOVE_ONE_CARD = 1
        MOVE_HELPER_CARD = 2
        MOVE_TO_ACE = 3
        FLIP_NEXT_HELPERS = 4

        if choice == TERMINATE:
            # print("Game Terminated")
            # print(self)
            return False

        elif choice == MOVE_ENTIRE_STACK:
            if not (self.SolitaireStacks[fromStack].faceUpStack):
                # print("Cannot move from empty stack")
                # print(self)
                return False
            highFromCard = self.SolitaireStacks[fromStack].highFaceUpCard()

            if (highFromCard.getRank() == 13) and not (
                self.SolitaireStacks[toStack].faceUpStack
            ):
                self.SolitaireStacks[toStack].addFaceUpCardStack(
                    self.SolitaireStacks[fromStack].removeFaceUpStack()
                )
                # print(self)
                return True

            if not self.SolitaireStacks[toStack].faceUpStack:
                # print("Cannot move to an empty stack without a king")
                # print(self)
                return False

            lowToCard = self.SolitaireStacks[toStack].lowFaceUpCard()
            if (lowToCard.getColor() is not highFromCard.getColor()) and (
                highFromCard.getRank() + 1 == lowToCard.getRank()
            ):
                self.SolitaireStacks[toStack].addFaceUpCardStack(
                    self.SolitaireStacks[fromStack].removeFaceUpStack()
                )
                # print(self)
                return True
            else:
                # print("That is not a valid move")
                # print(self)
                return False

        elif choice == MOVE_ONE_CARD:
            if not self.SolitaireStacks[fromStack].faceUpStack:
                # print("cannot move from empty stack")
                # print(self)
                return False

            movingCard = self.SolitaireStacks[fromStack].lowFaceUpCard()
            if movingCard.getRank() == 13:
                if not self.SolitaireStacks[toStack].faceUpStack:
                    self.SolitaireStacks[toStack].addFaceUpCardStack(
                        self.SolitaireStacks[fromStack].removeFaceUpStack()
                    )
                    # print(self)
                    return True
                else:
                    # print("Cannot move a king to a nonempty stack")
                    # print(self)
                    return False

            lowToCard = self.SolitaireStacks[toStack].lowFaceUpCard()
            if (lowToCard.getColor() is not movingCard.getColor()) and (
                movingCard.getRank() + 1 == lowToCard.getRank()
            ):
                self.SolitaireStacks[toStack].addFaceUpCard(
                    self.SolitaireStacks[fromStack].removeTopCard()
                )
                # print(self)
                return True
            else:
                # print("Cannot push ", str(movingCard), " to ", str(lowToCard))
                return False

        elif choice == MOVE_HELPER_CARD:
            if not self.helpStack.faceUpStack:
                # print("Cannot move from an empty stack")
                # print(self)
                return False
            movingCard = self.helpStack.lowFaceUpCard()

            # means we need to move the card to an ace stack
            if toStack == -1:
                # checking to see if the card is an ace, then pushing the ace to a new ace stack
                if movingCard.getRank() == 1:
                    newAceStack = AceStack()
                    newAceStack.addFaceUpCard(
                        self.helpStack.removeTopCard(revealTop=False)
                    )
                    self.aceStacks.append(newAceStack)
                    # print(self)
                    return True

                for aceStack in self.aceStacks:
                    topAceCard = aceStack.lowFaceUpCard()
                    # print(f'moving {movingCard} to {topAceCard}')
                    # print(f'move rank: {movingCard.rank}; suit: {movingCard.suit}')
                    # print(f'ace Rank: {topAceCard.rank}; suit: {topAceCard.suit}')
                    if (topAceCard.getSuit() == movingCard.getSuit()) and (
                        topAceCard.getRank() == movingCard.getRank() - 1
                    ):
                        aceStack.addFaceUpCard(
                            self.helpStack.removeTopCard(revealTop=False)
                        )
                        # print(self)
                        return True
                # print("Cannot move this card to the ace stacks")
                return False
            # check to see if it's a king
            if movingCard.getRank() == 13:
                if not self.SolitaireStacks[toStack].faceUpStack:
                    self.SolitaireStacks[toStack].addFaceUpCard(
                        self.helpStack.removeTopCard()
                    )
                    return True
                else:
                    # print("Cannot move a king to a nonempty stack")
                    return False
                # print(self)
                return
            # if its not an ace, and not a king, use the regular code for moving a card
            lowToCard = self.SolitaireStacks[toStack].lowFaceUpCard()
            if (lowToCard.getColor() is not movingCard.getColor()) and (
                movingCard.getRank() + 1 == lowToCard.getRank()
            ):
                self.SolitaireStacks[toStack].addFaceUpCard(
                    self.helpStack.removeTopCard()
                )
                # print(self)
                return True
            else:
                # print("Cannot push ", str(movingCard), " to ", str(lowToCard))
                return False

        elif choice == MOVE_TO_ACE:
            if not self.SolitaireStacks[fromStack].faceUpStack:
                # print("Cannot move from empty stack")
                # print(self)
                return False

            movingCard = self.SolitaireStacks[fromStack].lowFaceUpCard()
            # print("moving ", str(movingCard), str(movingCard.rank))
            if movingCard.getRank() == 1:
                # print("Moving Ace")
                newAceStack = AceStack()
                newAceStack.addFaceUpCard(
                    self.SolitaireStacks[fromStack].removeTopCard()
                )
                self.aceStacks.append(newAceStack)
                # print(self)
                return True

            for aceStack in self.aceStacks:
                topAceCard = aceStack.lowFaceUpCard()
                # print(f"trying to move to {topAceCard}")
                if (topAceCard.getRank() == movingCard.getRank() - 1) and (
                    topAceCard.getSuit() == movingCard.getSuit()
                ):
                    aceStack.addFaceUpCard(
                        self.SolitaireStacks[fromStack].removeTopCard()
                    )
                    # print(self)
                    return True

            # print("Could not find an ace stack to push ", str(movingCard), " to")
            return False

        elif choice == FLIP_NEXT_HELPERS:
            if not self.helpStack.faceDownStack:
                self.helpStack.flipOver()
            self.helpStack.revealTopThreeCards()
            return True
            # print(self)

    def checkWin(self):
        win = True
        if len(self.aceStacks) != 4:
            return False

        for stack in self.aceStacks:
            # print(stack.lowFaceUpCard())
            if stack.lowFaceUpCard().rank != 13:
                win = False
        return win
