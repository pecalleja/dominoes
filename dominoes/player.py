from dataclasses import dataclass, field


@dataclass()
class Player:
    name: str
    pieces: list = field(default_factory=list)

    def start_piece(self):
        doubles = [x for x in self.pieces if x[0] == x[1]]
        doubles.sort()
        high_double = doubles[-1]
        self.pieces.remove(high_double)
        return high_double
