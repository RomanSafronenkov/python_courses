from random import randint


class Cell:
    def __init__(self):
        self.__is_mine: bool = False
        self.__number: int = 0
        self.__is_open: bool = False

    @property
    def is_mine(self):
        return self.__is_mine

    @is_mine.setter
    def is_mine(self, flg):
        if isinstance(flg, bool):
            self.__is_mine = flg
        else:
            raise ValueError("недопустимое значение атрибута")

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, number):
        if isinstance(number, int) and 0 <= number <= 8:
            self.__number = number
        else:
            raise ValueError("недопустимое значение атрибута")

    @property
    def is_open(self):
        return self.__is_open

    @is_open.setter
    def is_open(self, flg):
        if isinstance(flg, bool):
            self.__is_open = flg
        else:
            raise ValueError("недопустимое значение атрибута")

    def __bool__(self):
        return not self.is_open


class GamePole:
    CREATED_OBJECT = None

    def __new__(cls, *args, **kwargs):
        """Singleton"""
        if cls.CREATED_OBJECT is None:
            obj = object.__new__(cls)
            cls.CREATED_OBJECT = obj

        return cls.CREATED_OBJECT

    def __init__(self, n: int, m: int, total_mines: int):
        self.n = n  # rows
        self.m = m  # cols
        self.total_mines = total_mines
        self.mines_indxs = []
        self._pole_cells = [[Cell() for i in range(m)] for j in range(n)]

    @property
    def pole(self):
        return self._pole_cells

    def init_pole(self):
        total_cells = self.n * self.m
        mines_idxs = []

        # generate mines
        i = 0
        while i != self.total_mines:
            idx = randint(0, total_cells)
            if idx not in mines_idxs:
                mines_idxs.append(idx)
                i += 1
        self.mines_indxs = mines_idxs

        # find neighbors for each cell
        for idx in range(total_cells):
            # i, j index of cell
            i, j = idx // self.m, idx % self.m

            if idx in mines_idxs:
                self.pole[i][j].is_mine = True

            neighbors = []
            for c in [-1, 0, 1]:  # previous, current, next row
                n_idx = idx + c * self.m
                if not 0 <= n_idx <= total_cells:
                    continue
                n_idx_neg = n_idx - 1  # left from the value in the row
                n_idx_pos = n_idx + 1  # right from the value in the row

                row_idx = n_idx // self.m  # which row we observe

                # range of values in this row
                row_min, row_max = row_idx * self.m, (row_idx + 1) * self.m - 1

                neighs = [n_idx_neg, n_idx, n_idx_pos]
                neighs = [n for n in neighs if (row_min <= n <= row_max) and (n != idx) and (0 <= n <= total_cells)]

                neighbors.extend(neighs)

            # count mines around each cell
            for n in neighbors:
                if n in mines_idxs:
                    self.pole[i][j].number = self.pole[i][j].number + 1

    def open_cell(self, i, j):
        if not (0 <= i <= self.n - 1) or not (0 <= j <= self.m - 1):
            raise IndexError('некорректные индексы i, j клетки игрового поля')
        self.pole[i][j].is_open = True

    def show_pole(self):
        result = '   ' + ' '.join(list(map(str, range(self.m)))) + '\n'
        for i, row in enumerate(self.pole):
            row_string = f"{i}| "
            for cell in row:
                if cell.is_open:
                    symbol = "*" if cell.is_mine else str(cell.number)
                else:
                    symbol = '#'
                row_string += symbol + ' '
            row_string = row_string[:-1] + '\n'
            result += row_string
        print(result)

    def check_pole(self):
        sum_closed = 0
        for row in self.pole:
            for cell in row:
                if cell:
                    sum_closed += 1
        return sum_closed == len(self.mines_indxs)


if __name__ == '__main__':
    test = False
    if test:
        p1 = GamePole(10, 20, 10)
        p2 = GamePole(10, 20, 10)
        assert id(p1) == id(p2), "создается несколько объектов класса GamePole"
        p = p1

        cell = Cell()
        assert type(Cell.is_mine) == property and type(Cell.number) == property and type(
            Cell.is_open) == property, "в классе Cell должны быть объекты-свойства is_mine, number, is_open"

        cell.is_mine = True
        cell.number = 5
        cell.is_open = True
        assert bool(cell) == False, "функция bool() вернула неверное значение"

        try:
            cell.is_mine = 10
        except ValueError:
            assert True
        else:
            assert False, "не сгенерировалось исключение ValueError"

        try:
            cell.number = 10
        except ValueError:
            assert True
        else:
            assert False, "не сгенерировалось исключение ValueError"

        p.init_pole()
        m = 0
        for row in p.pole:
            for x in row:
                assert isinstance(x, Cell), "клетками игрового поля должны быть объекты класса Cell"
                if x.is_mine:
                    m += 1

        assert m == 10, "на поле расставлено неверное количество мин"
        p.open_cell(0, 1)
        p.open_cell(9, 19)

        try:
            p.open_cell(10, 20)
        except IndexError:
            assert True
        else:
            assert False, "не сгенерировалось исключение IndexError"


        def count_mines(pole, i, j):
            n = 0
            for k in range(-1, 2):
                for l in range(-1, 2):
                    ii, jj = k + i, l + j
                    if ii < 0 or ii > 9 or jj < 0 or jj > 19:
                        continue
                    if pole[ii][jj].is_mine:
                        n += 1

            return n


        for i, row in enumerate(p.pole):
            for j, x in enumerate(row):
                if not p.pole[i][j].is_mine:
                    m = count_mines(p.pole, i, j)
                    assert m == p.pole[i][j].number, "неверно подсчитано число мин вокруг клетки"
    else:
        print('Игра Сапер')
        n, m = list(map(int, input('Введите число строк и столбцов через пробел: ').split()))

        num_mines = randint(n * m // 5, n * m // 3)
        print(f'Число мин: {num_mines}')

        game = GamePole(n, m, num_mines)
        game.init_pole()

        while True:
            i, j = list(map(int, input('Введите i, j индексы ячейки: ').split()))

            try:
                game.open_cell(i, j)
            except IndexError as e:
                print(e)
                continue

            game.show_pole()
            if (i * game.m + j) in game.mines_indxs:
                print('Вы проиграли')
                break

            if game.check_pole():
                print('Вы выиграли! УРА!!!')
                break
