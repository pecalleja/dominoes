import random
from player import Player


class Stock:
    pieces: list

    def __init__(self):
        self.pieces = []
        for x in range(0, 7):
            for y in range(x, 7):
                self.pieces.append([x, y])

    def randomize(self):
        random.shuffle(self.pieces)

    def draw_random_piece(self, player: Player, amount=1):
        # TODO: what if stock is empty ?
        for _ in range(amount):
            piece = random.choice(self.pieces)
            player.pieces.append(piece)
            self.pieces.remove(piece)
