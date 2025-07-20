class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):
        return f'Книга: {self.title}; {self.author}; {self.pages}'


# lst_in = list(map(str.strip, sys.stdin.readlines()))
# book = Book(*lst_in)
# print(book)

# ----------------------------
class Model:
    def __init__(self):
        self.data = {}

    def query(self, **kwargs):
        self.data = kwargs

    def __str__(self):
        string = 'Model'
        if self.data:
            string += ': '
            for key, value in self.data.items():
                string += f'{key} = {value}, '
            string = string[:-2]
        return string


model = Model()
model.query(id=1, fio='Sergey', old=33)
print(model)


# ----------------------------
class WordString:
    def __init__(self, string=''):
        self.__string = ''

        self.string = string
        self.__splitted_string = self.string.split()

    def __len__(self):
        return len(self.__splitted_string)

    @property
    def string(self):
        return self.__string

    @string.setter
    def string(self, string):
        self.__string = string
        self.__splitted_string = string.split()

    def __call__(self, indx):
        return self.__splitted_string[indx]


words = WordString()
words.string = "Курс по Python ООП"
n = len(words)
first = "" if n == 0 else words(0)
print(words.string)
print(f"Число слов: {n}; первое слово: {first}")


# ----------------------------
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_obj(self, obj):
        if self.tail is not None:
            self.tail.next = obj
            obj.prev = self.tail
            self.tail = obj
        else:
            self.head = self.tail = obj

    def remove_obj(self, indx):
        obj = self[indx]
        prev_obj = obj.prev
        next_obj = obj.next

        if prev_obj is not None:
            prev_obj.next = next_obj
        else:
            self.head = next_obj
        if next_obj is not None:
            next_obj.prev = prev_obj
        else:
            self.tail = prev_obj

    def __getitem__(self, item):
        i = 0
        cur = self.head
        while i != item:
            cur = cur.next
            i += 1
        return cur

    def __len__(self):
        cur = self.head
        count = 0
        while cur is not None:
            count += 1
            cur = cur.next
        return count

    def __call__(self, indx):
        return self[indx].data


class ObjList:
    def __init__(self, data):
        self.__data = data
        self.__prev = None
        self.__next = None

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    @property
    def prev(self):
        return self.__prev

    @prev.setter
    def prev(self, obj):
        self.__prev = obj

    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, obj):
        self.__next = obj

    def __str__(self):
        return f'ObjList: {self.data}'


linked_lst = LinkedList()
linked_lst.add_obj(ObjList("Sergey"))
linked_lst.add_obj(ObjList("Balakirev"))
linked_lst.add_obj(ObjList("Python"))
linked_lst.remove_obj(2)
linked_lst.add_obj(ObjList("Python ООП"))
n = len(linked_lst)  # n = 3
s = linked_lst(1)  # s = Balakirev
print(n, s)
print(linked_lst[0], linked_lst[1], linked_lst[2], sep='; ')


# ----------------------------
from math import sqrt

class Complex:
    def __init__(self, real, img):
        self.__real = real
        self.__img = img

    @staticmethod
    def check_num(num):
        return type(num) in [int, float]

    @property
    def real(self):
        return self.__real

    @real.setter
    def real(self, num):
        if not self.check_num(num):
            raise ValueError("Неверный тип данных.")
        self.__real = num

    @property
    def img(self):
        return self.__img

    @img.setter
    def img(self, num):
        if not self.check_num(num):
            raise ValueError("Неверный тип данных.")
        self.__img = num

    def __abs__(self):
        return sqrt(self.real * self.real + self.img * self.img)


cmp = Complex(7, 8)
cmp.real = 3
cmp.img = 4
c_abs = abs(cmp)
print(c_abs)

# ----------------------------
from math import sqrt


class RadiusVector:
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], int):
            self.__coords = [0 for i in range(args[0])]
        else:
            self.__coords = list(args)

    def set_coords(self, *args):
        for i, coord in zip(range(len(self)), args):
            self.__coords[i] = coord

    def get_coords(self):
        return tuple(self.__coords)

    def __len__(self):
        return len(self.__coords)

    def __abs__(self):
        return sqrt(sum([coord * coord for coord in self.__coords]))


vector3D = RadiusVector(3)
vector3D.set_coords(3, -5.6, 8)
a, b, c = vector3D.get_coords()
print(a, b, c)
vector3D.set_coords(3, -5.6, 8, 10, 11)  # ошибки быть не должно, последние две координаты игнорируются
vector3D.set_coords(1, 2)  # ошибки быть не должно, меняются только первые две координаты
res_len = len(vector3D)  # res_len = 3
res_abs = abs(vector3D)
print(res_len, res_abs)


# ----------------------------
class DeltaClock:
    def __init__(self, clock1, clock2):
        self.clock1 = clock1
        self.clock2 = clock2
        self.diff = clock1 - clock2

    def __str__(self):
        seconds = self.diff if self.diff > 0 else 0
        return self.format_seconds(seconds)

    def __len__(self):
        return self.diff if self.diff > 0 else 0

    @staticmethod
    def format_seconds(value):
        hours = value // 3600
        minutes = (value - hours * 3600) // 60
        seconds = value - hours * 3600 - minutes * 60

        result = ""
        for v in [hours, minutes, seconds]:
            result += f'0{v}' if v < 10 else str(v)
            result += ': '

        return result[:-2]


class Clock:
    def __init__(self, hours, minutes, seconds):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def get_time(self):
        return self.hours * 3600 + self.minutes * 60 + self.seconds

    def __sub__(self, other):
        return self.get_time() - other.get_time()


dt = DeltaClock(Clock(2, 45, 0), Clock(1, 15, 0))
print(dt)  # 01: 30: 00
len_dt = len(dt)  # 5400
print(len_dt)

# ----------------------------
class Ingredient:
    def __init__(self, name, volume, measure):
        self.name = name
        self.volume = volume
        self.measure = measure

    def __str__(self):
        return f"{self.name}: {self.volume}, {self.measure}"

class Recipe:
    def __init__(self, *args):
        self.__ingredients = list(args)

    def add_ingredient(self, ing):
        self.__ingredients.append(ing)

    def remove_ingredient(self, ing):
        self.__ingredients.remove(ing)

    def get_ingredients(self):
        return tuple(self.__ingredients)

    def __len__(self):
        return len(self.__ingredients)

recipe = Recipe()
recipe.add_ingredient(Ingredient("Соль", 1, "столовая ложка"))
recipe.add_ingredient(Ingredient("Мука", 1, "кг"))
recipe.add_ingredient(Ingredient("Мясо баранины", 10, "кг"))
ings = recipe.get_ingredients()
n = len(recipe) # n = 3
print(ings, n)

# ----------------------------
class PolyLine:
    def __init__(self, start_coord, *args):
        self.start_coord = start_coord
        self.coords = list(args)

    def add_coord(self, *args):
        self.coords.append(args)

    def remove_coord(self, indx):
        del self.coords[indx-1]

    def get_coords(self):
        return tuple([self.start_coord]+self.coords)
