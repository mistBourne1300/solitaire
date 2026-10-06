import os

from card import Card
from SolitaireGame import SolitaireGame

if __name__ == "__main__":
    newDeck = [Card(s, i) for i in range(1, 14) for s in ["S", "H", "C", "D"]]
    
    newGame = SolitaireGame(newDeck)
    print("\n\n\n")
    print(newGame)
    playerChoice = 100
    fromStack = 0
    toStack = 0
    TERMINATE = -1
    MOVE_ENTIRE_STACK = 0
    MOVE_ONE_CARD = 1
    MOVE_HELPER_CARD = 2
    MOVE_TO_ACE = 3
    FLIP_NEXT_HELPERS = 4

    while (newGame.checkWin()) or playerChoice >= 0:
        print("checkWin(): ", str(newGame.checkWin()))
        print("playerChoice: ", str(playerChoice))
        playerChoice = int(
            input(
                "Enter your choice \n\t-1:Terminate, \n\t 0:Move Entire Stack, \n\t 1:Move One Card, \n\t 2:Move Helper Card, \n\t 3:Move To Ace, \n\t 4:Flip Next Helpers, \n\t 5:Print Game (debugging)\n"
            )
        )
        if playerChoice == TERMINATE or playerChoice == FLIP_NEXT_HELPERS:
            newGame.makeMove(playerChoice)
        elif playerChoice == MOVE_ENTIRE_STACK or playerChoice == MOVE_ONE_CARD:
            fromStack = int(input("Enter the stack to move from: "))
            toStack = int(input("Enter the stack to move to (-1 for aces): "))
            newGame.makeMove(playerChoice, fromStack, toStack)
        elif playerChoice == MOVE_HELPER_CARD:
            toStack = int(input("Enter the stack to move to (-1 for aces): "))
            newGame.makeMove(playerChoice, fromStack, toStack)
        elif playerChoice == MOVE_TO_ACE:
            fromStack = int(input("Enter the stack to move from: "))
            newGame.makeMove(playerChoice, fromStack)
        elif playerChoice == 5:
            print(newGame)
            input("press enter to continue")
        else:
            print("Not a valid choice, try again: ")
        # input("press enter to continue")
        os.system("clear")
        print(newGame)
    print(newGame.checkWin())
    print(playerChoice)
    print("End of Program")
