from dataclasses import dataclass, field


@dataclass()
class Snake:
    elements: list = field(default_factory=list)

    def add_left(self, piece):
        if piece[-1] != self.elements[0][0]:
            a, b = piece[-1], piece[0]
            self.elements.insert(0, [a, b])
        else:
            a, b = piece[0], piece[-1]
            self.elements.insert(0, [a, b])

    def add_right(self, piece):
        if self.elements:
            if piece[0] != self.elements[-1][-1]:
                a, b = piece[-1], piece[0]
                self.elements.append([a, b])
            else:
                a, b = piece[0], piece[-1]
                self.elements.append([a, b])
        else:
            self.elements.append(piece)

    def endings(self):
        head = self.elements[0]
        if len(self.elements) > 1:
            tail = self.elements[-1]
            return head + tail
        else:
            return head

    def __str__(self):
        if len(self.elements) > 6:
            first_three = "".join(str(x) for x in self.elements[:3])
            last_three = "".join(str(x) for x in self.elements[-3:])
            msg = f"{first_three}...{last_three}"
            return msg
        else:
            return "".join(str(x) for x in self.elements)
