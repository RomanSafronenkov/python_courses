class Book:
    def __init__(self, title, author, pages, year):
        self.title = title
        self.author = author
        self.pages = pages
        self.year = year

class DigitBook(Book):
    def __init__(self, title, author, pages, year, size, frm):
        super().__init__(title, author, pages, year)
        self.size = size
        self.frm = frm


print('*'*20, ' Book ', '*'*20)
book = DigitBook('A', 'B', 10, 1999, 3, 'pdf')
print(book.__dict__)

# -----------------------------------------------

class Thing:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

class ArtObject(Thing):
    def __init__(self, name, weight, author, date):
        super().__init__(name, weight)
        self.author = author
        self.date = date

class Computer(Thing):
    def __init__(self, name, weight, memory, cpu):
        super().__init__(name, weight)
        self.memory = memory
        self.cpu = cpu

class Auto(Thing):
    def __init__(self, name, weight, dims):
        super().__init__(name, weight)
        self.dims = dims

class Mercedes(Auto):
    def __init__(self, name, weight, dims, model, old):
        super().__init__(name, weight, dims)
        self.model = model
        self.old = old

class Toyota(Auto):
    def __init__(self, name, weight, dims, model, wheel):
        super().__init__(name, weight, dims)
        self.model = model
        self.wheel = wheel

# -----------------------------------------------

class SellItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class House(SellItem):
    def __init__(self, name, price, material, square):
        super().__init__(name, price)
        self.material = material
        self.square = square

class Flat(SellItem):
    def __init__(self, name, price, size, rooms):
        super().__init__(name, price)
        self.size = size
        self.rooms = rooms

class Land(SellItem):
    def __init__(self, name, price, square):
        super().__init__(name, price)
        self.square = square

class Agency:
    def __init__(self, name):
        self.name = name
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        del self.objects[self.objects.index(obj)]

    def get_objects(self):
        return self.objects
    
print('*'*20, ' Agency ', '*'*20)
ag = Agency("Рога и копыта")
ag.add_object(Flat("квартира, 3к", 10000000, 121.5, 3))
ag.add_object(Flat("квартира, 2к", 8000000, 74.5, 2))
ag.add_object(Flat("квартира, 1к", 4000000, 54, 1))
ag.add_object(House("дом, крипичный", price=35000000, material="кирпич", square=186.5))
ag.add_object(Land("участок под застройку", 3000000, 6.74))
for obj in ag.get_objects():
    print(obj.name)

lst_houses = [x for x in ag.get_objects() if isinstance(x, House)] # выделение списка домов

# -----------------------------------------------

class Router:
    app = {}

    @classmethod
    def get(cls, path):
        return cls.app.get(path)

    @classmethod
    def add_callback(cls, path, func):
        cls.app[path] = func

class Callback:
    def __init__(self, path, route_cls):
        self.path = path
        self.route_cls = route_cls
        
    def __call__(self, func):
        self.route_cls.add_callback(self.path, func)
        return func


@Callback('/', Router)
def index():
    return '<h1>Главная</h1>'

print('*'*20, ' Router ', '*'*20)
route = Router.get('/')
if route:
    ret = route()
    print(ret)

# -----------------------------------------------

def integer_params_decorated(v):
    def wrapper(*args):
        _, other_args = args[0], args[1:]
        for arg in other_args:
            if not isinstance(arg, int):
                raise TypeError("аргументы должны быть целыми числами")
        return v(*args)
    return wrapper

def integer_params(cls):
    methods = {k: v for k, v in cls.__dict__.items() if callable(v)}
    for k, v in methods.items():
        print(k, v)
        setattr(cls, k, integer_params_decorated(v))

    return cls

@integer_params
class Vector:
    def __init__(self, *args):
        self.__coords = list(args)

    def __getitem__(self, item):
        return self.__coords[item]

    def __setitem__(self, key, value):
        self.__coords[key] = value

    def set_coords(self, *coords, reverse=False):
        c = list(coords)
        self.__coords = c if not reverse else c[::-1]

print('*'*20, ' integer_params_decorated ', '*'*20)
vector = Vector(1, 2)
print(vector[1])
try:
    vector[1] = 20.4 # TypeError
except TypeError as e:
    print(e)

# -----------------------------------------------

class SoftList(list):
    def __getitem__(self, idx):
        if abs(idx) >= len(self):
            return False
        return super().__getitem__(idx)
    
print('*'*20, ' SoftList ', '*'*20)
sl = SoftList("python")
print(sl[0]) # 'p'
print(sl[-1]) # 'n'
print(sl[6]) # False
print(sl[-7]) # False

# -----------------------------------------------

class StringDigit(str):
    def __init__(self, string):
        if not string.isdigit():
            raise ValueError("в строке должны быть только цифры")
        super().__init__()

    def __add__(self, other):
        result = super().__add__(other)
        return StringDigit(result)
    
    def __radd__(self, other):
        result = other.__add__(self)
        return StringDigit(result)

print('*'*20, ' StringDigit ', '*'*20)
sd = StringDigit("123")
assert str(sd) == "123", "неверно работает метод __str__ класса StringDigit"

try:
    sd2 = StringDigit("123a")
except ValueError:
    assert True
else:
    assert False, "не сгенерировалось исключение ValueError"


sd = sd + "345"
assert sd == "123345", "неверно отработал оператор +"

sd = "0" + sd
assert sd == "0123345", "неверно отработал оператор +"

try:
    sd = sd + "12d"
except ValueError:
    assert True
else:
    assert False, "не сгенерировалось исключение ValueError при выполнении оператора +"
    
try:
    sd = "12d" + sd
except ValueError:
    assert True
else:
    assert False, "не сгенерировалось исключение ValueError при выполнении оператора +"

# -----------------------------------------------

class ItemAttrs:
    def __getitem__(self, idx):
        keys = list(self.__dict__.keys())
        return self.__dict__[keys[idx]]

    def __setitem__(self, idx, value):
        keys = list(self.__dict__.keys())
        self.__dict__[keys[idx]] = value

class Point(ItemAttrs):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

print('*'*20, ' Point ', '*'*20)

pt = Point(1, 2.5)
x = pt[0]   # 1
y = pt[1]   # 2.5
print(x, y)
pt[0] = 10

print(pt.x, pt.y)