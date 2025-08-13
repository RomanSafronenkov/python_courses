import random


class TicTacToe:
    FREE_CELL = 0  # свободная клетка
    HUMAN_X = 1  # крестик (игрок - человек)
    COMPUTER_O = 2  # нолик (игрок - компьютер)

    def __init__(self):
        self.pole = None
        self.__is_human_win = None
        self.__is_computer_win = None
        self.__is_draw = None

        self.init()

    def init(self):
        self.__is_human_win = False
        self.__is_computer_win = False
        self.__is_draw = False
        self.pole = tuple(tuple(Cell() for i in range(3)) for j in range(3))

    @staticmethod
    def __check_idx(item):
        row, col = item
        if not isinstance(row, int) \
                or not isinstance(col, int) \
                or not (0 <= row < 3) \
                or not (0 <= col < 3):
            raise IndexError('некорректно указанные индексы')

    def __getitem__(self, item):
        self.__check_idx(item)
        cell = self.pole[item[0]][item[1]]
        return cell.value

    def __setitem__(self, key, value):
        self.__check_idx(key)
        self.pole[key[0]][key[1]].value = value

        is_win = self.__check_win(value)
        if is_win:
            if value == 1:
                self.is_human_win = True
            elif value == 2:
                self.is_computer_win = True

    def show(self):
        print('*' * 14)
        string = "\t0\t1\t2\n"
        for i, row in enumerate(self.pole):
            string += f'{i}\t' + '\t'.join(list(map(str, row))) + '\n'
        print(string[:-1])

    def __check_win(self, value):
        # check rows
        for row in self.pole:
            unique_values = list(set([cell.value for cell in row]))
            if len(unique_values) == 1 and unique_values[0] == value:
                return True

        # check cols
        for i in range(3):
            unique_values = []
            for row in self.pole:
                unique_values.append(row[i].value)

            unique_values = list(set(unique_values))
            if len(unique_values) == 1 and unique_values[0] == value:
                return True

        # check cross
        if self[0, 0] == self[1, 1] == self[2, 2] == value \
                or self[0, 2] == self[1, 1] == self[2, 0] == value:
            return True

        return False

    def human_go(self):
        row, col = list(map(int,
                            input("Введите координаты для вашего хода через пробел: ").split(' ')))
        self[row, col] = self.HUMAN_X

    def __find_free_cells(self):
        free_cells = []
        for i, row in enumerate(self.pole):
            for j, cell in enumerate(row):
                if cell.value == self.FREE_CELL:
                    free_cells.append((i, j))
        return free_cells

    def computer_go(self):
        # get information of free cells
        free_cells = self.__find_free_cells()

        cell_to_go = random.choice(free_cells)
        self[*cell_to_go] = self.COMPUTER_O

    @property
    def is_human_win(self):
        return self.__is_human_win

    @is_human_win.setter
    def is_human_win(self, value):
        if not isinstance(value, bool):
            raise ValueError('bool value is required')
        self.__is_human_win = value

    @property
    def is_computer_win(self):
        return self.__is_computer_win

    @is_computer_win.setter
    def is_computer_win(self, value):
        if not isinstance(value, bool):
            raise ValueError('bool value is required')
        self.__is_computer_win = value

    @property
    def is_draw(self):
        return self.__is_draw

    @is_draw.setter
    def is_draw(self, value):
        if not isinstance(value, bool):
            raise ValueError('bool value is required')
        self.__is_draw = value

    def __bool__(self):
        is_over = self.is_computer_win or self.is_human_win or self.is_draw
        free_cells = self.__find_free_cells()
        is_over |= len(free_cells) == 0
        return not is_over


class Cell:
    SYMBOL_DICT = {
        0: "\u2212",
        1: "\u274C",
        2: "\u2B55"
    }

    def __init__(self):
        self.value = 0

    def __bool__(self):
        return self.value == 0

    def __repr__(self):
        return f"{self.SYMBOL_DICT[self.value]}"


if __name__ == '__main__':
    game = TicTacToe()
    game.init()
    step_game = 0
    while game:
        game.show()

        if step_game % 2 == 0:
            game.human_go()
        else:
            game.computer_go()

        step_game += 1

    game.show()

    if game.is_human_win:
        print("Поздравляем! Вы победили!")
    elif game.is_computer_win:
        print("Все получится, со временем")
    else:
        print("Ничья.")
