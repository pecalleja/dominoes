# Write your code here
from dataclasses import dataclass
from player import Player
from stock import Stock


class DominoesGame:
    stock: Stock
    players: list[Player]
    _max_pieces = 7
    starting: Player = None
    next: Player = None
    snake: list

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


@dataclass()
class DominoesGUI:
    game: DominoesGame
    user: str

    def render(self):
        print("="*70)
        print("Stock pieces:", len(self.game.stock.pieces))
        your_pieces = []
        for player in self.game.players:
            if player.name != self.user:
                print(f"{player.name} pieces:", len(player.pieces))
            else:
                your_pieces = player.pieces
        print()
        print(self.game.snake)
        print()
        print("Your pieces:")
        for index, piece in enumerate(your_pieces):
            print(f"{index+1}:{piece}")
        print()
        status_msg = "Status: "
        if self.game.next.name == self.user:
            status_msg += "It's your turn to make a move. Enter your command."
        else:
            status_msg += f"{self.game.next.name} is about to make a move. Press Enter to continue..."
        print(status_msg)


game = DominoesGame(Stock(), [Player("computer"), Player("player")])
gui = DominoesGUI(game=game, user="player")
initial_player = game.start()
game.snake = initial_player.start_piece()
gui.render()
