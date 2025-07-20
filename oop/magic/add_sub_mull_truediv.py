class NewList:
    def __init__(self, lst=None):
        self.__list = lst if lst is not None else []
        self.__dtypes = list(map(type, self.__list))

    def __sub__(self, other):
        sc = other
        if isinstance(other, NewList):
            sc = other.get_list()

        sc_types = list(map(type, sc))
        sc_and_types = list(zip(sc_types, sc))
        new_list = []
        for elem_type, elem in zip(self.__dtypes, self.__list):
            if (elem_type, elem) in sc_and_types:
                sc_and_types.remove((elem_type, elem))
            else:
                new_list.append(elem)

        return NewList(new_list)

    def __rsub__(self, other):
        return NewList(other) - self

    def get_list(self):
        return self.__list

    def __str__(self):
        return f'{self.__list}'


lst1 = NewList([1, 2, -4, 6, 10, 11, 15, False, True])
lst2 = NewList([0, 1, 2, 3, True])
res_1 = lst1 - lst2  # NewList: [-4, 6, 10, 11, 15, False]
print(res_1)
lst1 -= lst2  # NewList: [-4, 6, 10, 11, 15, False]
print(lst1)
res_2 = lst2 - [0, True]  # NewList: [1, 2, 3]
print(res_2)
res_3 = [1, 2, 3, 4.5] - res_2  # NewList: [4.5]
print(res_3)
a = NewList([2, 3])
res_4 = [1, 2, 2, 3] - a  # NewList: [1, 2]
print(res_4)


# --------------------------------
class ListMath:
    def __init__(self, lst=None):
        if lst is None:
            self.lst_math = []
        else:
            self.lst_math = [value for value in lst if type(value) in [int, float]]

    def __add__(self, other):
        lst = []
        for elem in self.lst_math:
            lst.append(elem + other)
        return ListMath(lst)

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        for i, elem in enumerate(self.lst_math):
            self.lst_math[i] = (elem + other)
        return self

    def __sub__(self, other):
        lst = []
        for elem in self.lst_math:
            lst.append(elem - other)
        return ListMath(lst)

    def __rsub__(self, other):
        return -1 * self + other

    def __isub__(self, other):
        for i, elem in enumerate(self.lst_math):
            self.lst_math[i] = (elem - other)
        return self

    def __mul__(self, other):
        lst = []
        for elem in self.lst_math:
            lst.append(elem * other)
        return ListMath(lst)

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        for i, elem in enumerate(self.lst_math):
            self.lst_math[i] = (elem * other)
        return self

    def __truediv__(self, other):
        lst = []
        for elem in self.lst_math:
            lst.append(elem / other)
        return ListMath(lst)

    def __rtruediv__(self, other):
        lst = []
        for elem in self.lst_math:
            lst.append(other / elem)
        return ListMath(lst)

    def __itruediv__(self, other):
        for i, elem in enumerate(self.lst_math):
            self.lst_math[i] = (elem / other)
        return self

    def __str__(self):
        return f'{self.lst_math}'


lst = ListMath([1, "abc", -5, 7.68, True])  # ListMath: [1, -5, 7.68]
print(lst)
lst = lst + 76  # сложение каждого числа списка с определенным числом
print(lst)
lst = 6.5 + lst  # сложение каждого числа списка с определенным числом
print(lst)
lst += 76.7  # сложение каждого числа списка с определенным числом
print(lst)
lst = lst - 76  # вычитание из каждого числа списка определенного числа
print(lst)
lst = 7.0 - lst  # вычитание из числа каждого числа списка
print(lst)
lst -= 76.3
print(lst)
lst = lst * 5  # умножение каждого числа списка на указанное число (в данном случае на 5)
print(lst)
lst = 5 * lst  # умножение каждого числа списка на указанное число (в данном случае на 5)
print(lst)
lst *= 5.54
print(lst)
lst = lst / 13  # деление каждого числа списка на указанное число (в данном случае на 13)
print(lst)
lst = 3 / lst  # деление числа на каждый элемент списка
print(lst)
lst /= 13.0
print(lst)


# --------------------------------
class Stack:
    def __init__(self):
        self.top = None

    def push_back(self, obj):
        if self.top is not None:
            cur = self.top
            while cur.next is not None:
                cur = cur.next
            cur.next = obj
        else:
            self.top = obj

    def pop_back(self):
        if self.top is not None:
            cur = self.top
            if cur.next is None:
                self.top = None
                return

            while cur.next.next is not None:
                cur = cur.next
            cur.next = None

    def __str__(self):
        lst = []
        cur = self.top
        while cur is not None:
            lst.append(cur.data)
            cur = cur.next
        return f"{lst}"

    def __add__(self, other):
        self.push_back(other)
        return self

    def __mul__(self, other):
        for data in other:
            obj = StackObj(data)
            self.push_back(obj)
        return self


class StackObj:
    def __init__(self, data):
        self.__data = data
        self.__next = None

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, obj):
        self.__next = obj


st = Stack()
st.push_back(StackObj(1))
st.push_back(StackObj(2))
st.push_back(StackObj(3))
print(st)
st.pop_back()
print(st)
st = st + StackObj(4)
print(st)
st += StackObj(5)
print(st)

st = st * ['data_1', 'data_2', ..., 'data_N']
print(st)
st *= ['data_1', 'data_2', ..., 'data_N']
print(st)


# --------------------------------
class Lib:
    def __init__(self):
        self.book_list = []

    def __add__(self, other):
        self.book_list += [other]
        return self

    def __sub__(self, other):
        if isinstance(other, int):
            del self.book_list[other]
        elif isinstance(other, Book):
            self.book_list.remove(other)
        return self

    def __len__(self):
        return len(self.book_list)


class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year


# --------------------------------
class Budget:
    def __init__(self):
        self.items = []

    def add_item(self, it):
        self.items.append(it)

    def remove_item(self, indx):
        del self.items[indx]

    def get_items(self):
        return self.items


class Item:
    def __init__(self, name, money):
        self.name = name
        self.money = money

    def __add__(self, other):
        sc = other
        if isinstance(other, Item):
            sc = other.money
        return self.money + sc

    def __radd__(self, other):
        return self + other


# --------------------------------
class Box3D:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth

    def __add__(self, other):
        width = self.width + other.width
        height = self.height + other.height
        depth = self.depth + other.depth
        return Box3D(width, height, depth)

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        width = self.width * other
        height = self.height * other
        depth = self.depth * other
        return Box3D(width, height, depth)

    def __rmul__(self, other):
        return self * other

    def __sub__(self, other):
        width = self.width - other.width
        height = self.height - other.height
        depth = self.depth - other.depth
        return Box3D(width, height, depth)

    def __floordiv__(self, other):
        width = self.width // other
        height = self.height // other
        depth = self.depth // other
        return Box3D(width, height, depth)

    def __mod__(self, other):
        width = self.width % other
        height = self.height % other
        depth = self.depth % other
        return Box3D(width, height, depth)

    def __str__(self):
        return f'{self.width}, {self.height}, {self.depth}'


box1 = Box3D(1, 2, 3)
box2 = Box3D(2, 4, 6)

box = box1 + box2  # Box3D: width=3, height=6, depth=9 (соответствующие размерности складываются)
print(box)
box = box1 * 2  # Box3D: width=2, height=4, depth=6 (каждая размерность умножается на 2)
print(box)
box = 3 * box2  # Box3D: width=6, height=12, depth=18
print(box)
box = box2 - box1  # Box3D: width=1, height=2, depth=3 (соответствующие размерности вычитаются)
print(box)
box = box1 // 2  # Box3D: width=0, height=1, depth=1 (соответствующие размерности целочисленно делятся на 2)
print(box)
box = box2 % 3  # Box3D: width=2, height=1, depth=0
print(box)


# --------------------------------
class MaxPooling:
    def __init__(self, step=(2, 2), size=(2, 2)):
        self.step = step
        self.size = size

    @staticmethod
    def check_matrix(matrix):
        is_valid = True
        num_cols = len(matrix[0])
        for row in matrix:
            is_valid &= len(row) == num_cols
            dtypes = list(map(type, row))
            is_valid &= all([dtype in [int, float] for dtype in dtypes])
        if not is_valid:
            raise ValueError("Неверный формат для первого параметра matrix.")

    @staticmethod
    def max_2d(matrix):
        row_maxes = []
        for row in matrix:
            row_max = max(row)
            row_maxes.append(row_max)
        return max(row_maxes)

    def create_slice(self, matrix, start_row, start_col):
        num_rows, num_cols = self.size
        if start_row + num_rows > self.h_in or start_col + num_cols > self.w_in:
            return []
        slice_ = []
        for row_i in range(start_row, start_row + num_rows):
            row = []
            for col_i in range(start_col, start_col + num_cols):
                row.append(matrix[row_i][col_i])
            slice_.append(row)
        return slice_

    def __call__(self, matrix):
        self.check_matrix(matrix)
        self.h_in = len(matrix)
        self.w_in = len(matrix[0])
        h_out = (self.h_in - self.size[0]) // self.step[0] + 1
        w_out = (self.w_in - self.size[1]) // self.step[1] + 1

        result = []
        step_row, step_col = self.step

        for i in range(h_out):
            row = []
            for j in range(w_out):
                start_row = i * step_row
                start_col = j * step_col
                slice_ = self.create_slice(matrix, start_row, start_col)
                max_ = self.max_2d(slice_)
                row.append(max_)
            result.append(row)

        return result


mp = MaxPooling()
matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]]
res = mp(matrix)  # [[6, 8], [9, 7]
print(res)
print(mp.create_slice(matrix, 2, 2))
