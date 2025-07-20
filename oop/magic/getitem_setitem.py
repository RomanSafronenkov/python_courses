class Record:
    def __init__(self, **kwargs):
        self._order = {}
        for i, (key, value) in enumerate(kwargs.items()):
            self.__dict__[key] = value
            self._order[i] = key

    def __getitem__(self, item):
        if item >= len(self._order):
            raise IndexError('неверный индекс поля')

        key = self._order[item]
        return self.__dict__[key]

    def __setitem__(self, key, value):
        if key >= len(self._order):
            raise IndexError('неверный индекс поля')

        key_ = self._order[key]
        self.__dict__[key_] = value


r = Record(pk=1, title='Python ООП', author='Балакирев')

r[0] = 2  # доступ к полю pk
r[1] = 'Супер курс по ООП'  # доступ к полю title
r[2] = 'Балакирев С.М.'  # доступ к полю author
print(r[1])  # Супер курс по ООП
try:
    r[3]  # генерируется исключение IndexError
except IndexError:
    print('IndexError')


# --------------------------
class Track:
    def __init__(self, start_x, start_y):
        self.start_x = start_x
        self.start_y = start_y
        self.segments = []

    def add_point(self, x, y, speed):
        self.segments.append((x, y, speed))

    def __check_index(self, item):
        if not isinstance(item, int) or not 0 <= item < len(self.segments):
            raise IndexError('некорректный индекс')

    def __getitem__(self, item):
        self.__check_index(item)
        x, y, speed = self.segments[item]
        return (x, y), speed

    def __setitem__(self, key, value):
        self.__check_index(key)
        x, y, speed = self.segments[key]
        self.segments[key] = (x, y, value)


tr = Track(10, -5.4)
tr.add_point(20, 0, 100)  # первый линейный сегмент: indx = 0
tr.add_point(50, -20, 80)  # второй линейный сегмент: indx = 1
tr.add_point(63.45, 1.24, 60.34)  # третий линейный сегмент: indx = 2

tr[2] = 60
c, s = tr[2]
print(c, s)

try:
    res = tr[3]  # IndexError
except IndexError:
    print('IndexError')


# --------------------------
class Array:
    def __init__(self, max_length, cell):
        self.array = [cell(0) for _ in range(max_length)]
        self.max_length = max_length

    def __check_index(self, item):
        if not isinstance(item, int) or not 0 <= item < self.max_length:
            raise IndexError('неверный индекс для доступа к элементам массива')

    def __getitem__(self, item):
        self.__check_index(item)

        return self.array[item].value

    def __setitem__(self, key, value):
        self.__check_index(key)

        self.array[key].value = value

    def __str__(self):
        array_values = [str(cell.value) for cell in self.array]
        return ' '.join(array_values)


class Integer:
    def __init__(self, start_value):
        self.__value = start_value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not isinstance(value, int):
            raise ValueError('должно быть целое число')
        self.__value = value


ar_int = Array(10, cell=Integer)
print(ar_int[3])
print(ar_int)  # должны отображаться все значения массива в одну строчку через пробел
ar_int[1] = 10
try:
    ar_int[1] = 10.5  # должно генерироваться исключение ValueError
except ValueError as e:
    print(e)

try:
    ar_int[10] = 1  # должно генерироваться исключение IndexError
except IndexError as e:
    print(e)

# --------------------------
class IntegerValue:
    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise ValueError('возможны только целочисленные значения')
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

class CellInteger:
    value = IntegerValue()

    def __init__(self, start_value=0):
        self.value = start_value

class TableValues:
    def __init__(self, rows, cols, cell=None):
        if cell is None:
            raise ValueError('параметр cell не указан')
        self.cells = [[cell() for i in range(cols)] for j in range(rows)]

    def __getitem__(self, item):
        if isinstance(item, tuple):
            return self.cells[item[0]][item[1]].value

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            self.cells[key[0]][key[1]].value = value


table = TableValues(2, 3, cell=CellInteger)
print(table[0, 1])
table[1, 1] = 10
try:
    table[0, 0] = 1.45 # генерируется исключение ValueError
except ValueError as e:
    print(e)

# вывод таблицы в консоль
for row in table.cells:
    for x in row:
        print(x.value, end=' ')
    print()

# --------------------------
class StackObj:
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    def __init__(self):
        self.top = None
        self.n_elems = 0

    def push(self, obj):
        if not self.top:
            self.top = obj
            self.n_elems += 1
            return

        cur_elem = self.top
        while cur_elem.next:
            cur_elem = cur_elem.next

        cur_elem.next = obj
        self.n_elems += 1

    def pop(self):
        if not self.top:
            return

        cur_elem = self.top
        if cur_elem.next is None:
            self.top = None
            self.n_elems -= 1
            return cur_elem

        while cur_elem.next.next:
            cur_elem = cur_elem.next

        obj = cur_elem.next
        cur_elem.next = None
        self.n_elems -= 1
        return obj

    def __len__(self):
        return self.n_elems

    def __check_index(self, i):
        if not (0 <= i < len(self)) or not isinstance(i, int):
            raise IndexError('неверный индекс')

    def __getitem__(self, idx):
        self.__check_index(idx)
        if self.n_elems == 0:
            return

        cur_elem = self.top
        i = 0
        while i != idx:
            cur_elem = cur_elem.next
            i += 1

        return cur_elem

    def __setitem__(self, idx, obj):
        self.__check_index(idx)

        if idx == 0:
            obj.next = self.top.next
            self.top = obj
            return

        prev_elem = self.top
        cur_elem = prev_elem.next
        i = 1
        while i != idx:
            prev_elem = cur_elem
            cur_elem = prev_elem.next
            i += 1

        prev_elem.next = obj
        prev_elem.next.next = cur_elem.next
        return

# --------------------------
class RadiusVector:
    def __init__(self, *args):
        self.coords = list(args)

    def __getitem__(self, idx):
        res = self.coords[idx]
        return res if not isinstance(res, list) else tuple(res)

    def __setitem__(self, idx, value):
        self.coords[idx] = value

# --------------------------
class Cell:
    def __init__(self):
        self.is_free = True
        self.value = 0  # 1 - крестик, 2 - нолик

    def __bool__(self):
        return self.is_free

    def __repr__(self):
        return f'Free: {self.is_free}, value: {self.value}'

class TicTacToe:
    def __init__(self):
        self.pole = tuple([Cell() for i in range(3)] for j in range(3))

    def clear(self):
        for row in self.pole:
            for cell in row:
                cell.is_free = True
                cell.value = 0

    def __getitem__(self, item):
        pole = list(self.pole)
        if isinstance(item, tuple):
            row_slice, col_slice = item
            rows = pole[row_slice]
            res = rows[col_slice]
        else:
            res = pole[item]
        return res if not isinstance(res, list) else tuple(res)


    def __setitem__(self, key, value):
        pass

game = TicTacToe()
game.clear()
print(game[:1, :1])

game[0, 0] = 1
game[1, 0] = 2