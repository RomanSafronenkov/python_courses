class ListInteger(list):
    def __init__(self, args):
        if not any([isinstance(x, int) for x in args]):
            raise TypeError('можно передавать только целочисленные значения')
        super().__init__(args)

    def append(self, object):
        if not isinstance(object, int):
            raise TypeError('можно передавать только целочисленные значения')
        return super().append(object)
    
    def __setitem__(self, idx, item):
        if not isinstance(item, int):
            raise TypeError('можно передавать только целочисленные значения')
        return super().__setitem__(idx, item)
    
print('*'*20, ' ListInteger ', '*'*20)
s = ListInteger((1, 2, 3))
s[1] = 10
s.append(11)
print(s)
try:
    s[0] = 10.5 # TypeError
except TypeError as e:
    print(e)

# -----------------------------------------------
class Thing:
    def __init__(self, name, price, weight):
        self.name = name
        self.price = price
        self.weight = weight

    def __hash__(self):
        return hash(f"{self.name}_{self.price}_{self.weight}")


class DictShop(dict):
    def __init__(self, things={}):
        if not isinstance(things, dict):
            raise TypeError('аргумент должен быть словарем')
        
        for key in things.keys():
            if not isinstance(key, Thing):
                raise TypeError('ключами могут быть только объекты класса Thing')
            
        super().__init__(things)

    def __setitem__(self, key, value):
        if not isinstance(key, Thing):
            raise TypeError('ключами могут быть только объекты класса Thing')
        return super().__setitem__(key, value)
    

print('*'*20, ' Things ', '*'*20)
th_1 = Thing('Лыжи', 11000, 1978.55)
th_2 = Thing('Книга', 1500, 256)
dict_things = DictShop()
dict_things[th_1] = th_1
dict_things[th_2] = th_2

print(hash(th_1), hash(th_2))

for x in dict_things:
    print(x.name)

try:
    dict_things[1] = th_1 # исключение TypeError
except TypeError as e:
    print(e)

# -----------------------------------------------
class Protists:
    def __init__(self, name, weight, old):
        self.name = name
        self.weight = weight
        self.old = old

class Plants(Protists):
    pass

class Animals(Protists):
    pass

class Mosses(Plants):
    pass

class Flowering(Plants):
    pass

class Worms(Animals):
    pass

class Mammals(Animals):
    pass

class Human(Mammals):
    pass

class Monkeys(Mammals):
    pass

class Monkey(Monkeys):
    pass

class Person(Human):
    pass

class Flower(Flowering):
    pass

class Worm(Worms):
    pass

lst_objs = [
    Monkey("мартышка", 30.4, 7),
    Monkey("шимпанзе", 24.6, 8),
    Person("Балакирев", 88, 34),
    Person("Верховный жрец", 67.5, 45),
    Flower("Тюльпан", 0.2, 1),
    Flower("Роза", 0.1, 2),
    Worm("червь", 0.01, 1),
    Worm("червь 2", 0.02, 1)
]

lst_animals = [obj for obj in lst_objs if isinstance(obj, Animals)]
lst_plants = [obj for obj in lst_objs if isinstance(obj, Plants)]
lst_mammals = [obj for obj in lst_objs if isinstance(obj, Mammals)]

print('*'*20, ' Protists ', '*'*20)
print(lst_animals)
print(lst_plants)
print(lst_mammals)

# -----------------------------------------------
class Tuple(tuple):
    def __add__(self, other):
        if not isinstance(other, tuple):
            other = tuple(other)
        return Tuple(super().__add__(other))
    
print('*'*20, ' Tuple ', '*'*20)
t = Tuple([1, 2, 3])
t = t + "Python"
print(t)   # (1, 2, 3, 'P', 'y', 't', 'h', 'o', 'n')
t = (t + "Python") + "ООП"
print(t)

# -----------------------------------------------
class VideoItem:
    def __init__(self, title, descr, path):
        self.title = title
        self.descr = descr
        self.path = path
        self.rating = VideoRating()

class VideoRating:
    def __init__(self):
        self.__rating = 0

    @property
    def rating(self):
        return self.__rating
    
    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not (0 <= value <= 5):
            raise ValueError('неверное присваиваемое значение')
        
        self.__rating = value

print('*'*20, ' VideoItem ', '*'*20)
v = VideoItem('Курс по Python ООП', 'Подробный курс по Python ООР', 'D:/videos/python_oop.mp4')
print(v.rating.rating) # 0
v.rating.rating = 5
print(v.rating.rating) # 5
title = v.title
descr = v.descr
try:
    v.rating.rating = 6  # ValueError
except ValueError as e:
    print(e)

# -----------------------------------------------
class IteratorAttrs:
    def __iter__(self):
        return ((key, value) for key, value in self.__dict__.items())
    
class SmartPhone(IteratorAttrs):
    def __init__(self, model, size, memory):
        self.model = model
        self.size = size
        self.memory = memory

print('*'*20, ' IteratorAttrs ', '*'*20)

phone = SmartPhone('model', 12, 128)
for attr, value in phone:
    print(attr, value)