class Person:
    def __init__(self, fio, job, old, salary, year_job):
        self.fio = fio
        self.job = job
        self.old = old
        self.salary = salary
        self.year_job = year_job

        self._value = -1
        self._order = {
            0: 'fio',
            1: 'job',
            2: 'old',
            3: 'salary',
            4: 'year_job'
        }

    def __check_idx(self, idx):
        if idx not in list(range(5)):
            raise IndexError('неверный индекс')

    def __getitem__(self, item):
        self.__check_idx(item)
        key = self._order[item]
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__check_idx(key)
        key = self._order[key]
        self.__dict__[key] = value

    def __iter__(self):
        self._value = -1
        return self

    def __next__(self):
        while self._value != 4:
            self._value += 1
            key = self._order[self._value]
            return self.__dict__[key]
        else:
            raise StopIteration

pers = Person('Гейтс Б.', 'бизнесмен', 61, 1000000, 46)
pers[0] = 'Балакирев С.М.'
print(pers.fio)
for v in pers:
    print(v)
try:
    pers[5] = 123 # IndexError
except IndexError as e:
    print(e)

# ------------------------------------------------------

class Stack:
    def __init__(self):
        self.top = None
        self.n_elements = 0

        self._value = 0

    def push_back(self, obj):
        if not self.top:
            self.top = obj
            self.n_elements += 1
            return

        cur_elem = self.top
        while cur_elem.next:
            cur_elem = cur_elem.next

        cur_elem.next = obj
        self.n_elements += 1

    def push_front(self, obj):
        top = self.top
        self.top = obj
        self.top.next = top

        self.n_elements += 1

    def __getitem__(self, item):
        self.__check_idx(item)

        for i, elem in enumerate(self):
            if i == item:
                return elem.data

    def __setitem__(self, key, value):
        self.__check_idx(key)

        for i, elem in enumerate(self):
            if i == key:
                elem.data = value
                return

    def __iter__(self):
        self._value = -1
        return self

    def __next__(self):
        if self._value == -1:
            self._value += 1
            return self.top

        cur_elem = self.top
        while cur_elem:
            cur_elem = cur_elem.next
            self._value += 1
            if self._value == len(self):
                raise StopIteration
            return cur_elem

    def __len__(self):
        return self.n_elements

    def __check_idx(self, idx):
        if not (0 <= idx < len(self)):
            raise IndexError('неверный индекс')

    def __repr__(self):
        string = ""
        cur_elem = self.top
        while cur_elem:
            string += str(cur_elem) + '->'
            cur_elem = cur_elem.next
        return string[:-2]


class StackObj:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        return f'StackObj(data={self.data})'

st = Stack()
st.push_back(StackObj("1"))
st.push_front(StackObj("2"))
print(st)
print(len(st))
print(st[0], st[1])

assert st[0] == "2" and st[1] == "1", "неверные значения данных из объектов стека, при обращении к ним по индексу"

st[0] = "0"
assert st[0] == "0", "получено неверное значение из объекта стека, возможно, некорректно работает присваивание нового значения объекту стека"

for obj in st:
    assert isinstance(obj, StackObj), "при переборе стека через цикл должны возвращаться объекты класса StackObj"

try:
    a = st[3]
except IndexError:
    assert True
else:
    assert False, "не сгенерировалось исключение IndexError"

# ------------------------------------------------------

class Cell:
    def __init__(self, data):
        self.__data = data

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

class TableValues:
    def __init__(self, rows, cols, type_data=int):
        self.values = [[Cell(0) for i in range(cols)] for j in range(rows)]
        self.type_data = type_data
        self.rows = rows
        self.cols = cols

        self._value = -1

    def __getitem__(self, item):
        self.__check_idx(item)
        return self.values[item[0]][item[1]].data

    def __setitem__(self, key, value):
        self.__check_idx(key)
        if not isinstance(value, self.type_data):
            raise TypeError('неверный тип присваиваемых данных')

        self.values[key[0]][key[1]].data = value

    def __iter__(self):
        self._value = -1
        return self

    def __next__(self):
        while True:
            self._value += 1
            if self._value >= self.rows:
                raise StopIteration
            return [val.data for val in self.values[self._value]]

    def __check_idx(self, idx):
        if not (0 <= idx[0] < self.rows) or not (0 <= idx[1] < self.cols):
            raise IndexError('неверный индекс')


tb = TableValues(3, 2)
n = m = 0
for row in tb:
    n += 1
    for value in row:
        m += 1
        assert type(
            value) == int and value == 0, "при переборе объекта класса TableValues с помощью вложенных циклов for, должен сначала возвращаться итератор для строк, а затем, этот итератор должен возвращать целые числа (значения соответствующих ячеек)"

assert n > 1 and m > 1, "неверно отработали вложенные циклы для перебора ячеек таблицы"

tb[0, 0] = 10
assert tb[0, 0] == 10, "не работает запись нового значения в ячейку таблицы"

try:
    tb[2, 0] = 5.2
except TypeError:
    assert True
else:
    assert False, "не сгенерировалось исключение TypeError"

try:
    a = tb[2, 4]
except IndexError:
    assert True
else:
    assert False, "не сгенерировалось исключение IndexError"

# ------------------------------------------------------
print("*"*20, 'Matrix', '*'*20)

class Matrix:
    def __init__(self, *args):
        if len(args) == 3:
            rows, cols, fill_value = args
            if not isinstance(rows, int)\
                    or not isinstance(cols, int)\
                    or not isinstance(fill_value, (int, float)):
                raise TypeError('аргументы rows, cols - целые числа; fill_value - произвольное число')
            self.matrix = [[fill_value for i in range(cols)] for j in range(rows)]
            self.rows = rows
            self.cols = cols

        elif len(args) == 1:
            matrix = args[0]
            rows = len(matrix)
            cols_lens = []

            for row in matrix:
                for i, val in enumerate(row):
                    if not isinstance(val, (int, float)):
                        raise TypeError('список должен быть прямоугольным, состоящим из чисел')
                cols_lens.append(i+1)

            if len(set(cols_lens)) != 1:
                raise TypeError('список должен быть прямоугольным, состоящим из чисел')

            self.matrix = matrix
            self.rows = rows
            self.cols = len(matrix[0])

    def __check_idx(self, item):
        row, col = item
        if not isinstance(row, int)\
                or not isinstance(col, int)\
                or not (0 <= row < self.rows)\
                or not (0 <= col < self.cols):
            raise IndexError('недопустимые значения индексов')


    def __getitem__(self, item):
        assert isinstance(item, tuple)
        self.__check_idx(item)
        row, col = item
        return self.matrix[row][col]

    def __setitem__(self, key, value):
        assert isinstance(key, tuple)
        self.__check_idx(key)
        if not isinstance(value, (int, float)):
            raise TypeError('значения матрицы должны быть числами')
        row, col = key
        self.matrix[row][col] = value

    def __check_matrix_shape(self, other):
        rows, cols = len(other), len(other[0])
        if rows != self.rows or cols != self.cols:
            raise ValueError('операции возможны только с матрицами равных размеров')

    def __add__(self, other):
        new_matrix = []
        if isinstance(other, Matrix):
            self.__check_matrix_shape(other.matrix)

            for i in range(self.rows):
                col = []
                for j in range(self.cols):
                    col.append(self[i, j] + other[i, j])

                new_matrix.append(col)


        elif isinstance(other, (int, float)):
            for i in range(self.rows):
                col = []
                for j in range(self.cols):
                    col.append(self[i, j] + other)
                new_matrix.append(col)

        return Matrix(new_matrix)

    def __sub__(self, other):
        new_matrix = []
        if isinstance(other, Matrix):
            self.__check_matrix_shape(other.matrix)

            for i in range(self.rows):
                col = []
                for j in range(self.cols):
                    col.append(self[i, j] - other[i, j])

                new_matrix.append(col)


        elif isinstance(other, (int, float)):
            for i in range(self.rows):
                col = []
                for j in range(self.cols):
                    col.append(self[i, j] - other)
                new_matrix.append(col)

        return Matrix(new_matrix)

list2D = [[1, 2], [3, 4], [5, 6, 7]]
try:
    st = Matrix(list2D)
except TypeError:
    assert True
else:
    assert False, "не сгенерировалось исключение TypeError для не прямоугольного списка в конструкторе Matrix"

list2D = [[1, []], [3, 4], [5, 6]]
try:
    st = Matrix(list2D)
except TypeError:
    assert True
else:
    assert False, "не сгенерировалось исключение TypeError для списка не из чисел в конструкторе Matrix"

try:
    st = Matrix('1', 2, 0)
except TypeError:
    assert True
else:
    assert False, "не сгенерировалось исключение TypeError для не числовых аргументов в конструкторе Matrix"

list2D = [[1, 2], [3, 4], [5, 6]]
matrix = Matrix(list2D)
assert matrix[2, 1] == 6, "неверно отработал конструктор или __getitem__"

matrix = Matrix(4, 5, 10)
assert matrix[3, 4] == 10, "неверно отработал конструктор или __getitem__"

try:
    v = matrix[3, -1]
except IndexError:
    assert True
else:
    assert False, "не сгенерировалось исключение IndexError"

try:
    v = matrix['0', 4]
except IndexError:
    assert True
else:
    assert False, "не сгенерировалось исключение IndexError"

matrix[0, 0] = 7
assert matrix[0, 0] == 7, "неверно отработал __setitem__"

try:
    matrix[0, 0] = 'a'
except TypeError:
    assert True
else:
    assert False, "не сгенерировалось исключение TypeError в __setitem__"

m1 = Matrix([[1, 2], [3, 4]])
m2 = Matrix([[1, 1], [1, 1], [1, 1]])

try:
    matrix = m1 + m2
except ValueError:
    assert True
else:
    assert False, "не сгенерировалось исключение ValueError при сложении матриц разных размеров"

m1 = Matrix([[1, 2], [3, 4]])
m2 = Matrix([[1, 1], [1, 1]])
matrix = m1 + m2
assert isinstance(matrix, Matrix), "операция сложения матриц должна возвращать экземпляр класса Matrix"
assert matrix[1, 1] == 5, "неверно отработала операция сложения матриц"
assert m1[1, 1] == 4 and m1[0, 1] == 2 and m2[1, 1] == 1 \
       and m2[0, 0] == 1, "исходные матрицы не должны меняться при операции сложения"

m1 = Matrix(2, 2, 1)
id_m1_old = id(m1)
m2 = Matrix(2, 2, 1)
m1 = m1 + m2
id_m1_new = id(m1)
assert id_m1_old != id_m1_new, "в результате операции сложения должен создаваться НОВЫЙ экземпляр класса Matrix"

matrix = Matrix(2, 2, 0)
m = matrix + 10
assert matrix[0, 0] == matrix[1, 1] == 0, "исходные матрицa не должна меняться при операции сложения c числом"
assert m[0, 0] == 10, "неверно отработала операция сложения матрицы с числом"

m1 = Matrix(2, 2, 1)
m2 = Matrix([[0, 1], [1, 0]])
identity_matrix = m1 - m2  # должна получиться единичная матрица
assert m1[0, 0] == 1 and m1[1, 1] == 1 and m2[0, 0] == 0 \
       and m2[0, 1] == 1, "исходные матрицы не должны меняться при операции вычитания"
assert identity_matrix[0, 0] == 1 and identity_matrix[1, 1] == 1, "неверно отработала операция вычитания матриц"

matrix = Matrix(2, 2, 1)
m = matrix - 1
assert matrix[0, 0] == matrix[1, 1] == 1, "исходные матрицa не должна меняться при операции вычитания c числом"
assert m[0, 0] == m[1, 1] == 0, "неверно отработала операция вычитания числа из матрицы"