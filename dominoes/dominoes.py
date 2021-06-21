# Write your code here
from dataclasses import dataclass
from player import Player, PlayerBehaviour, ComputerBehaviour
from stock import Stock
from snake import Snake
from abc import ABC, abstractmethod


class AbstractDominoesGui(ABC):

    @abstractmethod
    def render_turn(self, game):
        raise NotImplementedError

    def render_end(self, game):
        raise NotImplementedError


class DominoesGame:
    stock: Stock
    players: list[Player]
    _max_pieces = 7
    starting: Player = None
    next: Player = None
    snake: Snake
    winner: Player = None
    gui: AbstractDominoesGui

    def __init__(self, stock: Stock, players: list[Player], gui: AbstractDominoesGui):
        self.stock = stock
        self.players = players
        self.gui = gui

    def start(self):
        self.stock.randomize()
        self._initial_drawback()
        self.starting = self._chose_start_player()
        self.snake = Snake()
        self.snake.add_right(
            self.starting.start_piece()
        )
        self._game_loop()

    def _game_loop(self):
        while True:
            self.gui.render_turn(self)
            self.next.take_turn(self.snake, self.stock)
            if self._check_end_condition():
                self.gui.render_turn(self)
                self.gui.render_end(self)
                break

            index = self.players.index(self.next)
            self.next = self.players[index - 1]

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

    def _check_end_condition(self) -> bool:
        for player in self.players:
            if len(player.pieces) == 0:
                self.winner = player
                return True
        if len(self.snake.elements) >= 10:
            endings = self.snake.endings()
            all_snake = []
            for element in self.snake.elements:
                all_snake.append(element[0])
                all_snake.append(element[1])
            for number in endings:
                if all_snake.count(number) == 8:
                    return True
        return False


@dataclass()
class DominoesGUI(AbstractDominoesGui):
    user: str

    def render_turn(self, game: DominoesGame):
        print("="*70)
        print("Stock pieces:", len(game.stock.pieces))
        your_pieces = []
        for player in game.players:
            if player.name != self.user:
                print(f"{player.name} pieces:", len(player.pieces))
            else:
                your_pieces = player.pieces
        print()
        print(str(game.snake))
        print()
        print("Your pieces:")
        for index, piece in enumerate(your_pieces):
            print(f"{index+1}:{piece}")
        print()
        status_msg = "Status: "
        if game.next.name == self.user:
            status_msg += "It's your turn to make a move. Enter your command."
        else:
            status_msg += f"{game.next.name} is about to make a move. Press Enter to continue..."
        print(status_msg)

    def render_end(self, game: DominoesGame):
        status_msg = "Status: The game is over. "
        if game.winner:
            if game.winner.name == self.user:
                status_msg += "You won!"
            else:
                status_msg += f"The {game.winner.name} won!"
        else:
            status_msg += "It's a draw!"
        print(status_msg)


dominoes_game = DominoesGame(
    Stock(),
    [
        Player("computer", ComputerBehaviour()),
        Player("player", PlayerBehaviour())
    ],
    DominoesGUI(user="player")
)
dominoes_game.start()
