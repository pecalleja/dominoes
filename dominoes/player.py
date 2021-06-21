import random
from dataclasses import dataclass, field
from abc import ABC
from snake import Snake


class AbstractPlayerBehaviour(ABC):

    def make_a_move(self, player_pieces: list, snake: Snake) -> Snake:
        """
        Choice a pieces add to the snake based on the input and return the piece
        :param player_pieces:
        :param snake:
        :return:
        """
        raise NotImplementedError


@dataclass()
class Player:
    name: str
    behaviour: AbstractPlayerBehaviour
    pieces: list = field(default_factory=list)

    def start_piece(self):
        doubles = [x for x in self.pieces if x[0] == x[1]]
        doubles.sort()
        high_double = doubles[-1]
        self.pieces.remove(high_double)
        return high_double

    def take_turn(self, snake, stock):
        piece = self.behaviour.make_a_move(self.pieces, snake)
        if piece:
            self.pieces.remove(piece)
        else:
            stock.draw_random_piece(self, 1)
        return snake


class PlayerBehaviour(AbstractPlayerBehaviour):

    def make_a_move(self, player_pieces, snake):
        # command = 0
        # index = -8
        valid_input = False
        while not valid_input:
            try:
                command = int(input())
                index = abs(command) - 1
                if command != 0:
                    player_choice = player_pieces[index]
                    # found = False
                    # for tile in player_choice:
                    #     if command > 0 and tile in snake.elements[-1]:
                    #         found = True
                    #     if command < 0 and tile in snake.elements[0]:
                    #         found = True
                    # if not found:
                    #     raise ValueError("Pieces do not match with snake tail")
                valid_input = True
            except (ValueError, IndexError):
                print("Invalid input. Please try again.")
                valid_input = False

        if command > 0:
            snake.add_right(player_pieces[index])
        elif command < 0:
            snake.add_left(player_pieces[index])
        else:
            return None
        return player_pieces[index]


class ComputerBehaviour(AbstractPlayerBehaviour):
    def make_a_move(self, computer_pieces: list, snake):
        input()
        choice = random.choice(computer_pieces)
        side = random.choice(["-", "+"])
        if side == "+":
            snake.add_right(choice)
        else:
            snake.add_left(choice)
        return choice
