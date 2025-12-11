# -----------------------------------------------

class Student:
    def __init__(self, fio, group):
        self._fio = fio  # ФИО студента (строка)
        self._group = group # группа (строка)
        self._lect_marks = []  # оценки за лекции
        self._house_marks = []  # оценки за домашние задания

    def add_lect_marks(self, mark):
        self._lect_marks.append(mark)

    def add_house_marks(self, mark):
        self._house_marks.append(mark)

    def __str__(self):
        return f"Студент {self._fio}: оценки на лекциях: {str(self._lect_marks)}; оценки за д/з: {str(self._house_marks)}"


class Mentor:
    def __init__(self, fio, subject):
        self._fio = fio
        self._subject = subject

class Lector(Mentor):
    def set_mark(self, student, mark):
        student.add_lect_marks(mark)

    def __str__(self):
        return f"Лектор {self._fio}: предмет {self._subject}"

class Reviewer(Mentor):
    def set_mark(self, student, mark):
        student.add_house_marks(mark)

    def __str__(self):
        return f"Эксперт {self._fio}: предмет {self._subject}"

print('*'*20, ' Student-Mentor ', '*'*20)

lector = Lector("Балакирев С.М.", "Информатика")
reviewer = Reviewer("Гейтс Б.", "Информатика")
students = [Student("Иванов А.Б.", "ЭВМд-11"), Student("Гаврилов С.А.", "ЭВМд-11")]
persons = [lector, reviewer]
lector.set_mark(students[0], 4)
lector.set_mark(students[1], 2)
reviewer.set_mark(students[0], 5)
reviewer.set_mark(students[1], 3)
for p in persons + students:
    print(p)
# в консоли будет отображено:
# Лектор Балакирев С.М.: предмет Информатика
# Эксперт Гейтс Б.: предмет Информатика
# Студент Иванов А.Б.: оценки на лекциях: [4]; оценки за д/з: [5]
# Студент Гаврилов С.А.: оценки на лекциях: [2]; оценки за д/з: [3]

# -----------------------------------------------

class ShopInterface:
    def get_id(self):
        raise NotImplementedError('в классе не переопределен метод get_id')
    
class ShopItem(ShopInterface):
    NUM_CREATED = 0

    def __new__(cls, *args, **kwargs):
        new_obj = object.__new__(cls)
        new_obj.__id = ShopItem.NUM_CREATED
        ShopItem.NUM_CREATED += 1
        return new_obj

    def __init__(self, name, weight, price):
        super().__init__()
        self._name = name
        self._weight = weight
        self._price = price

    def get_id(self):
        return self.__id
    
print('*'*20, ' ShopItem ', '*'*20)

item1 = ShopItem("имя1", "вес1", "100")
item2 = ShopItem("имя2", "вес2", "200")
print(item1.get_id(), item1._name)
print(item2.get_id(), item2._name)

# -----------------------------------------------

class Validator:
    def _is_valid(self, data):
        raise NotImplementedError('в классе не переопределен метод _is_valid')
    
    def __call__(self, data):
        return self._is_valid(data)
    
class FloatValidator(Validator):
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def _is_valid(self, data):
        is_valid = True
        is_valid &= isinstance(data, float)
        if is_valid:
            is_valid &= self.min_value <= data <= self.max_value
        return is_valid

print('*'*20, ' Validator ', '*'*20)

float_validator = FloatValidator(0, 10.5)
res_1 = float_validator(1)  # False (целое число, а не вещественное)
res_2 = float_validator(1.0)  # True
res_3 = float_validator(-1.0)  # False (выход за диапазон [0; 10.5])
print(res_1, res_2, res_3)

# -----------------------------------------------
from abc import ABC, abstractmethod

class Model(ABC):
    @abstractmethod
    def get_pk(self):
        pass

    def get_info(self):
        return "Базовый класс Model"
    
class ModelForm(Model):
    def __init__(self, login, password):
        self._login = login
        self._password = password
        self._id = hash(login+password)

    def get_pk(self):
        return self._id

print('*'*20, ' Model ', '*'*20)
form = ModelForm("Логин", "Пароль")
print(form.get_pk())

# -----------------------------------------------

class StackInterface(ABC):
    @abstractmethod
    def push_back(self, obj):
        pass

    @abstractmethod
    def pop_back(self):
        pass

class Stack(StackInterface):
    def __init__(self):
        self._top = None

    def push_back(self, obj):
        if not self._top:
            self._top = obj
            return
        
        cur = self._top
        while cur._next:
            cur = cur._next

        cur._next = obj

    def pop_back(self):
        if not self._top:
            return
        
        if not self._top._next:
            obj = self._top
            self._top = None
            return obj

        cur = self._top
        
        while cur._next._next:
            cur = cur._next

        obj = cur._next
        cur._next = None
        return obj


class StackObj:
    def __init__(self, data):
        self._data = data
        self._next = None


print('*'*20, ' Stack ', '*'*20)
st = Stack()
print(st._top)
st.push_back(StackObj("obj 1"))
print(st._top._data)
obj = StackObj("obj 2")
st.push_back(obj)
print(st._top._data)

del_obj = st.pop_back() # del_obj - ссылка на удаленный объект (если объектов не было, то del_obj = None)
print(del_obj._data)

# -----------------------------------------------

class CountryInterface(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def population(self):
        pass

    @property
    @abstractmethod
    def square(self):
        pass

    @abstractmethod
    def get_info(self):
        pass

class Country(CountryInterface):
    def __init__(self, name, population, square):
        self.__name = name
        self.__population = population
        self.__square = square

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def population(self):
        return self.__population
    
    @population.setter
    def population(self, population):
        self.__population = population

    @property
    def square(self):
        return self.__square
    
    @square.setter
    def square(self, square):
        self.__square = square

    def get_info(self):
        return f"{self.name}: {self.square}, {self.population}"

print('*'*20, ' Abstract Property ', '*'*20)
country = Country("Россия", 140000000, 324005489.55)
name = country.name
pop = country.population
country.population = 150000000
country.square = 354005483.0
print(country.get_info()) # Россия: 354005483.0, 150000000

# -----------------------------------------------

class Track:
    def __init__(self, *args):
        if len(args) == 2 and not isinstance(args[0], PointTrack) and not isinstance(args[1], PointTrack):
            self.__points = [PointTrack(*args)]

        else:
            self.__points = list(args)

    @property
    def points(self):
        return tuple(self.__points)
    
    def add_back(self, pt):
        if isinstance(pt, PointTrack):
            self.__points.append(pt)

    def add_front(self, pt):
        if isinstance(pt, PointTrack):
            self.__points = [pt] + self.__points

    def pop_back(self):
        return self.__points.pop()

    def pop_front(self):
        pt = self.__points[0]
        if len(self.__points) > 1:
            self.__points = self.__points[1:]
        else: self.__points = []

        return pt


class PointTrack:
    def __init__(self, x, y):
        self.__check_type(x)
        self.__check_type(y)
        self.x = x
        self.y = y

    def __check_type(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('координаты должны быть числами')
        
    def __str__(self):
        return f"PointTrack: {self.x}, {self.y}"

print('*'*20, ' Track ', '*'*20)

tr = Track(PointTrack(0, 0), PointTrack(1.2, -0.5), PointTrack(2.4, -1.5))
tr.add_back(PointTrack(1.4, 0))
tr.pop_front()
for pt in tr.points:
    print(pt)

# -----------------------------------------------

class Food:
    def __init__(self, name, weight, calories):
        self._name = name
        self._weight = weight
        self._calories = calories

class BreadFood(Food):
    def __init__(self, name, weight, calories, white):
        super().__init__(name, weight, calories)
        self._white = white

class SoupFood(Food):
    def __init__(self, name, weight, calories, dietary):
        super().__init__(name, weight, calories)
        self._dietary = dietary

class FishFood(Food):
    def __init__(self, name, weight, calories, fish):
        super().__init__(name, weight, calories)
        self._fish = fish

print('*'*20, ' Food ', '*'*20)

bf = BreadFood("Бородинский хлеб", 34.5, 512, False)
sf = SoupFood("Черепаший суп", 520, 890.5, False)
ff = FishFood("Консерва рыбная", 340, 1200, "семга")
