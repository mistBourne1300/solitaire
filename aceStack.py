from SolitaireStack import SolitaireStack


class AceStack(SolitaireStack):
    def __str__(self):
        if len(self.faceUpStack) > 0:
            return str(self.faceUpStack[-1])
        return "0 of 0"
