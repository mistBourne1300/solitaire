import os
from random import shuffle

import numpy as np
from card import Card
from matplotlib import pyplot as plt
from scipy import stats
from SolitaireGame import SolitaireGame
from SolitaireStack import SolitaireStack
from tqdm import tqdm


class SolitaireAlgor:
    def __init__(self, game: SolitaireGame):
        self.game = game
        self.made_move = False
        self.give_up = False
        self.prev_move = None
        self.prev_to_card = None

    def can_move(self, move_card: Card, to_card: Card):
        """determines if the moving card can be placed on the other in the normal stacks

        Parameters:
                move_card (Card): the moving card

                to_card (Card): the card being placed onto

        Returns:
                (boolean): whether the moving card is able to be placed on the other in the normal stacks
        """
        if not move_card:
            return False

        if move_card.rank == 13 and not to_card:
            return True

        if not to_card:
            return False

        return move_card.rank == to_card.rank - 1 and move_card.color != to_card.color

    def can_ace_move(self, move_card: Card, to_card: Card):
        """determines if the moving card can be placed on the other in the ace stacks

        Parameters:
                move_card (Card): the moving card

                to_card (Card): the card being placed onto

        Returns:
                (boolean): whether the moving card is able to be placed on the other in the ace stacks
        """
        if not move_card:
            return False

        if move_card.rank == 1 and not to_card:
            return True

        if not to_card:
            return False

        return move_card.rank == to_card.rank + 1 and move_card.suit == to_card.suit

    def try_stacks_high(self):
        """loops through the stacks searching for a move. if one is found, it will make the move and return True. Otherwise returns false

        Returns:
                T/F (boolean): whether or not a move was made on the game
        """
        # print("try_stacks_high()")
        for i in range(
            len(self.game.SolitaireStacks) - 1, -1, -1
        ):  # loop through all the stacks, starting at index 6
            move_card = self.game.SolitaireStacks[i].highFaceUpCard()
            # print(f'i {i}: {move_card}')
            if move_card is None:
                continue
            if (
                move_card.rank == 13
                and self.game.SolitaireStacks[i].getFaceDownStackSize() == 0
            ):
                continue
            for j in range(
                len(self.game.SolitaireStacks)
            ):  # loop through all the stacks
                if i == j:
                    continue
                to_card = self.game.SolitaireStacks[j].lowFaceUpCard()
                # print(f'\tj {j}: {to_card}')
                if (move_card is not self.prev_move) and self.can_move(
                    move_card, to_card
                ):
                    # if the previous card to move was a king to an empty space, and the current card to move is a king to an empty space, quit
                    if self.prev_move:
                        if (
                            self.prev_move.rank == 13
                            and move_card.rank == 13
                            and not self.prev_to_card
                            and not to_card
                        ):
                            return False

                    if not self.game.makeMove(0, i, j):
                        print(f"failed to move {move_card} to {to_card}")
                        raise ValueError()
                    self.prev_move = move_card
                    self.prev_to_card = to_card
                    return True
        return False

    def try_stacks_low(self):
        """loops through the stacks' low cards looking for a move to the aces

        Returns:
                (boolean): whether a move to the aces was made
        """
        # print("try_stacks_low()")
        for i in range(len(self.game.SolitaireStacks) - 1, -1, -1):
            move_card = self.game.SolitaireStacks[i].lowFaceUpCard()
            if not move_card:
                continue
            # print(f'i {i}: {move_card}')
            if (
                move_card.rank == 1
            ):  # the card is an ace, we just need to move it to an empty stack
                if not self.game.makeMove(3, i):
                    raise ValueError()
                self.prev_move = move_card
                self.prev_to_card = None
                return True
            for j in range(len(self.game.aceStacks)):
                to_card = self.game.aceStacks[j].lowFaceUpCard()
                if self.can_ace_move(move_card, to_card):
                    if not self.game.makeMove(3, i):
                        raise ValueError()
                    self.prev_move = move_card
                    self.prev_to_card = to_card
                    return True
        return False

    def loop_through_helper(self):
        # print("loop_through_helper()")
        if not self.game.helpStack.faceUpStack:
            self.game.makeMove(4, 0, 0)
        if not self.game.helpStack.faceUpStack:
            return False

        num_times_went_through = 0
        while num_times_went_through < 2 or self.game.helpStack.faceDownStack:
            # input("press enter to continue: ")
            move_card = self.game.helpStack.lowFaceUpCard()
            # print(f'trying {move_card}')

            # print("trying aces")
            for i in range(
                len(self.game.aceStacks)
            ):  # check to see if the card can be moved to the ace stacks
                if move_card.rank == 1:
                    if not self.game.makeMove(2, 0, -1):
                        raise ValueError()
                    self.prev_move = move_card
                    self.prev_to_card = None
                    return True
                to_card = self.game.aceStacks[i].lowFaceUpCard()
                # print(f'\tto: {to_card}')
                if self.can_ace_move(move_card, to_card):
                    if not self.game.makeMove(2, 0, -1):
                        # print(f'failed to move {move_card} to {to_card}')
                        raise ValueError()
                    self.prev_move = move_card
                    self.prev_to_card = to_card
                    return True

            # print("trying solitaire stacks")
            for i in range(
                len(self.game.SolitaireStacks)
            ):  # check to see if the card can be moved to the regular stacks
                to_card = self.game.SolitaireStacks[i].lowFaceUpCard()
                # print(f'\tto: {to_card}')
                if (move_card is not self.prev_move) and self.can_move(
                    move_card, to_card
                ):
                    if not self.game.makeMove(2, 0, i):
                        # print(f'failed to move {move_card} to {to_card}')
                        raise ValueError()
                    self.prev_move = move_card
                    self.prev_to_card = to_card
                    return True

            self.game.makeMove(4, 0, 0)
            if not self.game.helpStack.faceDownStack:
                num_times_went_through += 1
                # print(f"{num_times_went_through} petc: ")

        return False

    def play(self, v=True):
        while not self.give_up and not self.game.checkWin():
            # input("press enter to continue: ")
            # os.system("clear")
            try:
                if self.try_stacks_low():
                    if v:
                        print(self.game)
                    continue
            except KeyboardInterrupt:
                print("threw error in self.try_stacks_low()")
                return self.game.checkWin()

            try:
                if self.try_stacks_high():
                    if v:
                        print(self.game)
                    continue
            except KeyboardInterrupt:
                print("threw error in self.try_stacks_high()")
                return self.game.checkWin()

            try:
                if not self.loop_through_helper():
                    self.give_up = True
            except KeyboardInterrupt:
                print("threw error in self.loop_through_helper()")
                return self.game.checkWin()
            if v:
                print(f"give up: {self.give_up}")
            if v:
                print(self.game)

        return self.game.checkWin()


def recover_deck(game: SolitaireGame):
    deck = []
    game.helpStack.flipOver()
    while len(game.helpStack.faceDownStack) > 0:
        deck.append(game.helpStack.faceDownStack.pop())
        # print(game)
        # input("press enter to continue: ")

    for i in range(len(game.SolitaireStacks)):
        while game.SolitaireStacks[i].getFaceUpStackSize() > 0:
            deck.append(game.SolitaireStacks[i].faceUpStack.pop())
            # print(game)
            # input("press enter to continue: ")

    for i in range(len(game.SolitaireStacks)):
        while game.SolitaireStacks[i].getFaceDownStackSize() > 0:
            deck.append(game.SolitaireStacks[i].faceDownStack.pop())
            # print(game)
            # input("press enter to continue: ")

    acecount = 0
    for i in range(len(game.aceStacks)):
        while game.aceStacks[i].getFaceUpStackSize() > 0:
            acecount += 1
            deck.append(game.aceStacks[i].faceUpStack.pop())
            # print(game)
            # input("press enter to continue: ")

    if acecount > 24:
        # need to see if there's actually an ace in the top 28 cards...
        foundace = False
        for i in range(28):
            if deck[i].rank == 1:
                foundace = True
        if foundace:
            deck = ace_split(deck)

    return deck


def ace_split(deck: list):
    temp = []
    idx = 27
    while deck[idx].rank != 1:
        temp.append(deck.pop(idx))
        idx -= 1
    while len(temp) > 0:
        deck.insert(0, temp.pop(0))
    return deck


if __name__ == "__main__":
    os.system("clear")
    num_sims = 10000
    games_until_win_recovery = []
    print("running recovery simulations...")
    for i in tqdm(range(num_sims)):
        win = False
        deck = [Card(s, i) for s in ["S", "H", "C", "D"] for i in range(1, 14)]
        game = SolitaireGame(deck)
        i = 0
        while not win:
            i += 1
            algor = SolitaireAlgor(game)
            win = algor.play(v=False)
            # input(f"game {i} complete. press enter to continue: ")
            deck = recover_deck(game)
            game = SolitaireGame(deck, shuf=False)

        # print(f"won after {i} games")
        games_until_win_recovery.append(i)

    # num_sims /=1000
    games_until_win_random = []
    print("running random simulations...")
    for i in tqdm(range(num_sims)):
        win = False
        deck = [Card(s, i) for s in ["S", "H", "C", "D"] for i in range(1, 14)]
        game = SolitaireGame(deck)
        while not win:
            i += 1
            algor = SolitaireAlgor(game)
            win = algor.play(v=False)
            deck = [Card(s, i) for s in ["S", "H", "C", "D"] for i in range(1, 14)]
            game = SolitaireGame(deck)
        games_until_win_random.append(i)

    print(f"recovery algorithm:")
    print(f"mean time until success: {np.mean(games_until_win_recovery)}")
    print(f"max time until success: {np.max(games_until_win_recovery)}")
    print(f"min time until success: {np.min(games_until_win_recovery)}")
    print(f"median time until success: {np.median(games_until_win_recovery)}")
    recoverymode = stats.mode(games_until_win_recovery, keepdims=False)
    print(
        f"mode time until success: {recoverymode[0]} with {recoverymode[1]} occurences"
    )
    print("\n")
    print(f"random play:")
    print(f"mean time until success: {np.mean(games_until_win_random)}")
    print(f"max time until success: {np.max(games_until_win_random)}")
    print(f"min time until success: {np.min(games_until_win_random)}")
    print(f"median time until success: {np.median(games_until_win_random)}")
    randommode = stats.mode(games_until_win_random, keepdims=False)
    print(f"mode time until success: {randommode[0]} with {randommode[1]} occurences")

    plt.hist(games_until_win_recovery, label="recovery", alpha=0.9)
    plt.hist(games_until_win_random, label="random", alpha=0.9)
    plt.title("comparison of recovery vs random play games until success")
    plt.legend()
    plt.show()
