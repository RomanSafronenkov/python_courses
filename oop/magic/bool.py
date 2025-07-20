import sys


class Player:
    def __init__(self, name, old, score):
        self.name = name
        self.old = int(old)
        self.score = int(score)

    def __bool__(self):
        return self.score > 0


# lst_in = list(map(str.strip, sys.stdin.readlines()))
# players = []
#
# for row in lst_in:
#     name, old, score = row.split('; ')
#     player = Player(name, old, score)
#     players.append(player)
#
# players_filtered = list(filter(bool, players))
# print(players_filtered)

# ------------------------------------
class MailBox:
    def __init__(self):
        self.inbox_list = []

    def receive(self):
        lst_in = list(map(str.strip, sys.stdin.readlines()))
        for row in lst_in:
            item = MailItem(*row.split('; '))
            self.inbox_list.append(item)


class MailItem:
    def __init__(self, mail_from, title, content):
        self.mail_from = mail_from
        self.title = title
        self.content = content
        self.is_read = False

    def set_read(self, fl_read):
        self.is_read = fl_read

    def __bool__(self):
        return self.is_read

# mail = MailBox()
# mail.receive()
#
# mail.inbox_list[0].set_read(True)
# mail.inbox_list[-1].set_read(True)
#
# inbox_list_filtered = list(filter(bool, mail.inbox_list))
# print(inbox_list_filtered)

# ------------------------------------
class Ellipse:
    def __init__(self, *args):
        if args:
            self.x1, self.y1, self.x2, self.y2 = args

    def __bool__(self):
        is_true = True
        for param in ['x1', 'y1', 'x2', 'y2']:
            is_true &= self.__dict__.get(param) is not None
        return is_true

    def get_coords(self):
        if self:
            return self.x1, self.y1, self.x2, self.y2
        else:
            raise AttributeError('нет координат для извлечения')

lst_geom = [Ellipse(), Ellipse(), Ellipse(1, 2, 4, 5), Ellipse(0, -1, 9, 10)]
for elem in lst_geom:
    if elem:
        print(elem.get_coords())

# ------------------------------------
class Vector:
    def __init__(self, *args):
        self.coords = list(args)

    def check_length(self, other):
        if len(self.coords) != len(other.coords):
            raise ArithmeticError('размерности векторов не совпадают')

    def __add__(self, other):
        coords = []
        if isinstance(other, Vector):
            self.check_length(other)
            for c1, c2 in zip(self.coords, other.coords):
                coords.append(c1+c2)
        elif isinstance(other, (int, float)):
            for c1 in self.coords:
                coords.append(c1+other)
        return Vector(*coords)

    def __sub__(self, other):
        coords = []
        if isinstance(other, Vector):
            self.check_length(other)
            for c1, c2 in zip(self.coords, other.coords):
                coords.append(c1 - c2)
        elif isinstance(other, (int, float)):
            for c1 in self.coords:
                coords.append(c1 - other)
        return Vector(*coords)

    def __mul__(self, other):
        coords = []
        if isinstance(other, Vector):
            self.check_length(other)
            for c1, c2 in zip(self.coords, other.coords):
                coords.append(c1 * c2)
        return Vector(*coords)

    def __iadd__(self, other):
        coords = []
        if isinstance(other, Vector):
            self.check_length(other)
            for c1, c2 in zip(self.coords, other.coords):
                coords.append(c1 + c2)
        elif isinstance(other, (int, float)):
            for c1 in self.coords:
                coords.append(c1 + other)
        self.coords = coords
        return self

    def __isub__(self, other):
        coords = []
        if isinstance(other, Vector):
            self.check_length(other)
            for c1, c2 in zip(self.coords, other.coords):
                coords.append(c1 - c2)
        elif isinstance(other, (int, float)):
            for c1 in self.coords:
                coords.append(c1 - other)
        self.coords = coords
        return self

    def __eq__(self, other):
        is_equal = True
        for c1, c2 in zip(self.coords, other.coords):
            is_equal &= (c1 == c2)
        return is_equal