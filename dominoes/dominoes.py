# Write your code here
import random


class Player:
    pieces: list

    def __init__(self, name: str):
        self.name = name
        self.pieces = []

    def start_piece(self):
        doubles = [x for x in self.pieces if x[0] == x[1]]
        doubles.sort()
        high_double = doubles[-1]
        self.pieces.remove(high_double)
        return high_double


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
        for _ in range(amount):
            piece = random.choice(self.pieces)
            player.pieces.append(piece)
            self.pieces.remove(piece)


class DominoesGame:
    stock: Stock
    players: list[Player]
    _max_pieces = 7
    starting: Player = None
    next: Player = None

    def __init__(self, stock: Stock, players: list[Player]):
        self.stock = stock
        self.players = players

    def start(self):
        self.stock.randomize()
        self._initial_drawback()
        return self._chose_start_player()

    def _initial_drawback(self):
        for player in self.players:
            self.stock.draw_random_piece(player, amount=self._max_pieces)

    def _chose_start_player(self):
        all_doubles = [x for player in self.players for x in player.pieces if x[0] == x[1]]
        if not all_doubles:
            return None
        all_doubles.sort()
        max_dominoes = all_doubles[-1]
        for index, player in enumerate(self.players):
            if max_dominoes in player.pieces:
                self.starting = player
                self.next = self.players[index-1]
                return player


game = DominoesGame(Stock(), [Player("computer"), Player("player")])
initial_player = game.start()
snake_piece = [initial_player.start_piece()]
print("Stock pieces:", game.stock.pieces)
print("Computer pieces:", game.players[0].pieces)
print("Player pieces:", game.players[1].pieces)
print("Domino snake:", snake_piece)
print("Status:", game.next.name)
