from SolitaireStack import SolitaireStack


class helperStack(SolitaireStack):
    def revealTopThreeCards(self):
        for i in range(3):
            if self.faceDownStack:
                self.faceUpStack.append(self.faceDownStack.pop())

    def flipOver(self):
        while self.faceUpStack:
            self.faceDownStack.append(self.faceUpStack.pop())

    def __str__(self):
        stack = ""
        if len(self.faceDownStack) > 0:
            stack += "??? | "
        topThree = self.faceUpStack[-3:]
        for card in topThree:
            stack += str(card)
            stack += " | "
        stack = stack[:-2]
        return stack
