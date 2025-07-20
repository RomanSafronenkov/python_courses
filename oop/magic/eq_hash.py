from llvmlite.binding import ValueKind


class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __hash__(self):
        return hash((self.width, self.height))

r1 = Rect(10, 5, 100, 50)
r2 = Rect(-10, 4, 100, 50)

h1, h2 = hash(r1), hash(r2)   # h1 == h2
print(h1, h2)

# -----------------------------------
import sys
from ast import literal_eval

class ShopItem:
    def __init__(self, name, weight, price):
        self.name = name
        self.weight = weight
        self.price = price

    def __hash__(self):
        return hash((self.name.lower(), self.weight, self.price))

    def __eq__(self, other):
        return hash(self) == hash(other)

# lst_in = list(map(str.strip, sys.stdin.readlines()))
# shop_items = {}
#
# for row in lst_in:
#     indx_sep = row.find(':')
#     name = row[:indx_sep]
#     weight, price = list(map(literal_eval, row[indx_sep+2:].split()))
#     item = ShopItem(name, weight, price)
#
#     value = shop_items.get(item)
#     if value is None:
#         shop_items[item] = [item, 1]
#     else:
#         shop_items[item][1] += 1
# print(shop_items)

# -----------------------------------
class DataBase:
    def __init__(self, path):
        self.path = path
        self.dict_db = {}

    def write(self, record):
        if record not in self.dict_db:
            self.dict_db[record] = [record]
        else:
            self.dict_db[record].append(record)

    def read(self, pk):
        for rec, values in self.dict_db.items():
            for row in values:
                if row.pk == pk:
                    return row

class Record:
    INDEX = 0

    def __init__(self, fio, descr, old):
        self.fio = fio
        self.descr = descr
        self.old = old
        self.pk = Record.INDEX

        Record.INDEX += 1

    def __hash__(self):
        return hash((self.fio.lower(), self.old))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return f"Record: {self.fio}, {self.old}"

# lst_in = list(map(str.strip, sys.stdin.readlines()))
#
# db = DataBase('link')
#
# for row in lst_in:
#     row = row.split('; ')
#     row[-1] = int(row[-1])
#     record = Record(*row)
#     db.write(record)
#
# print(db.dict_db)

# -----------------------------------
class BookStudy:
    def __init__(self, name, author, year):
        self.name = name
        self.author = author
        self.year = year

    def __hash__(self):
        return hash((self.name.lower(), self.author.lower()))

    def __eq__(self, other):
        return hash(self) == hash(other)

# lst_in = list(map(str.strip, sys.stdin.readlines()))
#
# unique_books = []
#
# for row in lst_in:
#     row = row.split('; ')
#     row[-1] = int(row[-1])
#     unique_books.append(BookStudy(*row))
#
# unique_books = len(set(unique_books))

# -----------------------------------
class Dimensions:
    def __init__(self, a, b, c):
        if a < 0 or b < 0 or c < 0:
            raise ValueError("габаритные размеры должны быть положительными числами")
        self.a = a
        self.b = b
        self.c = c

    def __hash__(self):
        return hash((self.a, self.b, self.c))

# s_inp = input()
# lst_dims = []
#
# for row in s_inp.split('; '):
#     row = list(map(literal_eval, row.split()))
#     lst_dims.append(Dimensions(*row))
#
# lst_dims = sorted(lst_dims, key=lambda x: hash(x))
# print(lst_dims)

# -----------------------------------
from math import sqrt

class Value:
    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __set__(self, instance, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("длины сторон треугольника должны быть положительными числами")

        if self.name == '_a':
            value1 = instance.__dict__.get('_b')
            value2 = instance.__dict__.get('_c')

        elif self.name == '_b':
            value1 = instance.__dict__.get('_a')
            value2 = instance.__dict__.get('_c')

        elif self.name == '_c':
            value1 = instance.__dict__.get('_a')
            value2 = instance.__dict__.get('_b')

        if (value1 is not None) and (value2 is not None):
            if value >= value1 + value2 or value1 >= value + value2 or value2 >= value + value1:
                raise ValueError("с указанными длинами нельзя образовать треугольник")

        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]


class Triangle:
    a = Value()
    b = Value()
    c = Value()

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        if a >= b + c or b >= a + c or c >= a + b:
            raise ValueError("с указанными длинами нельзя образовать треугольник")

    def __len__(self):
        return int(self.a+self.b+self.c)

    def __call__(self):
        p = (self.a+self.b+self.c)/2
        return sqrt(p * (p-self.a) * (p-self.b) * (p-self.c))

# tr = Triangle(3, 5, 5)
# print(tr())
# tr.a = 40