class SmartPhone:
    def __init__(self, model):
        self.model = model
        self.apps = []
        self._app_types = []

    def add_app(self, app):
        if type(app) not in self._app_types:
            self.apps.append(app)
            self._app_types.append(type(app))

    def remove_app(self, app):
        self.apps.remove(app)
        self._app_types.remove(type(app))


class AppVK:
    def __init__(self):
        self.name = "ВКонтакте"


class AppYouTube:
    def __init__(self, memory_max):
        self.name = "YouTube"
        self.memory_max = memory_max


class AppPhone:
    def __init__(self, phone_list):
        self.name = "Phone"
        self.phone_list = phone_list


sm = SmartPhone("Honor 1.0")
sm.add_app(AppVK())
sm.add_app(AppVK())  # второй раз добавляться не должно
sm.add_app(AppYouTube(2048))
for a in sm.apps:
    print(a.name)


# ------------------------------
class Circle:
    def __init__(self, x, y, radius):
        self.__x = x
        self.__y = y
        self.__radius = radius

    @property
    def x(self):
        print("x getter")
        return self.__x

    @x.setter
    def x(self, x):
        print('x.setter')
        self.__x = x

    @property
    def y(self):
        print('y.getter')
        return self.__y

    @y.setter
    def y(self, y):
        print('y.setter')
        self.__y = y

    @property
    def radius(self):
        print('radius.getter')
        return self.__radius

    @radius.setter
    def radius(self, radius):
        print('radius.setter')
        self.__radius = radius

    def __setattr__(self, key, value):
        print(f'__setattr__ with key={key}, value={value}')
        if type(value) not in [int, float]:
            raise TypeError("Неверный тип присваиваемых данных.")

        if key == 'radius' and value < 0:
            return

        object.__setattr__(self, key, value)

    def __getattr__(self, item):
        print(f'__getattr__ with unknown key={item}')
        return False


circle = Circle(10.5, 7, 22)
circle.radius = -10  # прежнее значение не должно меняться, т.к. отрицательный радиус недопустим
x, y = circle.x, circle.y
res = circle.name  # False, т.к. атрибут name не существует
print(x, y, res)
circle.x = 20
x, y = circle.x, circle.y
print(x, y)


# ------------------------------
class Dimensions:
    MIN_DIMENSION = 10
    MAX_DIMENSION = 1000

    def __init__(self, a, b, c):
        self.__a = a
        self.__b = b
        self.__c = c

    @property
    def a(self):
        return self.__a

    @a.setter
    def a(self, a):
        self.__a = a

    @property
    def b(self):
        return self.__b

    @b.setter
    def b(self, b):
        self.__b = b

    @property
    def c(self):
        return self.__c

    @c.setter
    def c(self, c):
        self.__c = c

    def __setattr__(self, key, value):
        if key in ['MIN_DIMENSION', 'MAX_DIMENSION']:
            raise AttributeError("Менять атрибуты MIN_DIMENSION и MAX_DIMENSION запрещено.")

        if key in ['a', 'b', 'c'] and not self.MIN_DIMENSION <= value <= self.MAX_DIMENSION:
            return

        super().__setattr__(key, value)


d = Dimensions(10.5, 20.1, 30)
d.a = 8
d.b = 15
a, b, c = d.a, d.b, d.c  # a=10.5, b=15, c=30
try:
    d.MAX_DIMENSION = 10  # исключение AttributeError
except AttributeError as e:
    print(e)


# ------------------------------
import time
class Mechanical:
    def __init__(self, date):
        self.is_set = False
        self.date = date
        self.is_set = True

    def __setattr__(self, key, value):
        if key == 'date' and self.is_set:
            return

        super().__setattr__(key, value)


class Aragon:
    def __init__(self, date):
        self.is_set = False
        self.date = date
        self.is_set = True

    def __setattr__(self, key, value):
        if key == 'date' and self.is_set:
            return

        super().__setattr__(key, value)


class Calcium:
    def __init__(self, date):
        self.is_set = False
        self.date = date
        self.is_set = True

    def __setattr__(self, key, value):
        if key == 'date' and self.is_set:
            return

        super().__setattr__(key, value)


class GeyserClassic:
    MAX_DATE_FILTER = 100

    def __init__(self):
        self.slots = {i: None for i in range(1, 4)}

    def add_filter(self, slot_num, filter):
        if slot_num == 1 and isinstance(filter, Mechanical) and not self.slots[slot_num]:
            self.slots[slot_num] = filter

        elif slot_num == 2 and isinstance(filter, Aragon) and not self.slots[slot_num]:
            self.slots[slot_num] = filter

        elif slot_num == 3 and isinstance(filter, Calcium) and not self.slots[slot_num]:
            self.slots[slot_num] = filter

    def remove_filter(self, slot_num):
        self.slots[slot_num] = None

    def get_filters(self):
        f1 = self.slots[1]
        f2 = self.slots[2]
        f3 = self.slots[3]
        return tuple(filter(lambda x: x is not None, [f1, f2, f3]))

    def water_on(self):
        if not self.slots[1] or not self.slots[2] or not self.slots[3]:
            return False
        is_on = True
        for slot_n in range(1, 4):
            is_on &= (0 <= time.time() - self.slots[slot_n].date <= self.MAX_DATE_FILTER)

        return is_on

my_water = GeyserClassic()
my_water.add_filter(1, Mechanical(time.time()))
my_water.add_filter(2, Aragon(time.time()))
w = my_water.water_on() # False
print(w)
print(my_water.slots[1])
my_water.add_filter(3, Calcium(time.time()))
w = my_water.water_on() # True
print(w)
f1, f2, f3 = my_water.get_filters()  # f1, f2, f3 - ссылки на соответствующие объекты классов фильтров
my_water.add_filter(3, Calcium(time.time())) # повторное добавление в занятый слот невозможно
my_water.add_filter(2, Calcium(time.time())) # добавление в "чужой" слот также невозможно
print(f1, f2, f3)
print(my_water.slots[1].date)

my_water = GeyserClassic()
my_water.add_filter(1, Mechanical(time.time()))
my_water.add_filter(2, Aragon(time.time()))

assert my_water.water_on() == False, "метод water_on вернул True, хотя не все фильтры были установлены"

my_water.add_filter(3, Calcium(time.time()))
assert my_water.water_on(), "метод water_on вернул False при всех трех установленных фильтрах"

f1, f2, f3 = my_water.get_filters()
print(f1, f2, f3)
assert isinstance(f1, Mechanical) and isinstance(f2, Aragon) and isinstance(f3, Calcium), "фильтры должны быть устанлены в порядке: Mechanical, Aragon, Calcium"

my_water.remove_filter(1)
assert my_water.water_on() == False, "метод water_on вернул True, хотя один из фильтров был удален"

my_water.add_filter(1, Mechanical(time.time()))
assert my_water.water_on(), "метод water_on вернул False, хотя все три фильтра установлены"

f1, f2, f3 = my_water.get_filters()
my_water.remove_filter(1)

my_water.add_filter(1, Mechanical(time.time() - GeyserClassic.MAX_DATE_FILTER - 1))
assert my_water.water_on() == False, "метод water_on вернул True, хотя у одного фильтра истек срок его работы"

f1 = Mechanical(1.0)
f2 = Aragon(2.0)
f3 = Calcium(3.0)
assert 0.9 < f1.date < 1.1 and 1.9 < f2.date < 2.1 and 2.9 < f3.date < 3.1, "неверное значение атрибута date в объектах фильтров"

f1.date = 5.0
f2.date = 5.0
f3.date = 5.0

assert 0.9 < f1.date < 1.1 and 1.9 < f2.date < 2.1 and 2.9 < f3.date < 3.1, "локальный атрибут date в объектах фильтров должен быть защищен от изменения"

