# -----------------------------------------------

class Animal:
    def __init__(self, name, kind, old):
        self.__name = name
        self.__kind = kind
        self.__old = old

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def kind(self):
        return self.__kind
    
    @kind.setter
    def kind(self, value):
        self.__kind = value

    @property
    def old(self):
        return self.__old
    
    @old.setter
    def old(self, value):
        self.__old = value


print('*'*20, ' Animal ', '*'*20)
animals = [
    Animal("Васька", "дворовый кот", 5),
    Animal("Рекс", "немецкая овчарка", 8),
    Animal("Кеша", "попугай", 3)
]

# -----------------------------------------------

class Furniture:
    def __init__(self, name, weight):
        self.__verify_name(name)
        self.__verify_weight(weight)
        self._name = name
        self._weight = weight

    def __verify_name(self, name):
        if not isinstance(name, str):
            raise TypeError('название должно быть строкой')

    def __verify_weight(self, weight):
        if not isinstance(weight, (int, float)) or weight <= 0:
            raise TypeError('вес должен быть положительным числом')
        
    def __setattr__(self, name, value):
        if name == '_name':
            self.__verify_name(value)
        elif name == '_weight':
            self.__verify_weight(value)
        super().__setattr__(name, value)
    
    def get_attrs(self):
        return tuple(self.__dict__.values())


class Closet(Furniture):
    def __init__(self, name, weight, tp, doors):
        super().__init__(name, weight)
        self._tp = tp
        self._doors = doors


class Chair(Furniture):
    def __init__(self, name, weight, height):
        super().__init__(name, weight)
        self._height = height


class Table(Furniture):
    def __init__(self, name, weight, height, square):
        super().__init__(name, weight)
        self._height = height
        self._square = square


print('*'*20, ' Furniture ', '*'*20)
furniture = Furniture('closet', 15)
print(furniture.__dict__)
furniture.nnn = 'uuu'
furniture._name = 'not a closet'
print(furniture.__dict__)
try:
    furniture._name = 4
except TypeError as e:
    print(e)

cl = Closet('шкаф-купе', 342.56, True, 3)
chair = Chair('стул', 14, 55.6)
tb = Table('стол', 34.5, 75, 10)
print(tb.get_attrs())

# -----------------------------------------------

class Observer:
    def update(self, data):
        pass

    def __hash__(self):
        return hash(id(self))


class Subject:
    def __init__(self):
        self.__observers = {}
        self.__data = None

    def add_observer(self, observer):
        self.__observers[observer] = observer

    def remove_observer(self, observer):
        if observer in self.__observers:
            self.__observers.pop(observer)

    def __notify_observer(self):
        for ob in self.__observers:
            ob.update(self.__data)

    def change_data(self, data):
        self.__data = data
        self.__notify_observer()


class Data:
    def __init__(self, temp, press, wet):
        self.temp = temp    # температура
        self.press = press  # давление
        self.wet = wet      # влажность


# здесь объявляйте дочерние классы TemperatureView, PressureView и WetView
class TemperatureView(Observer):
    def update(self, data):
        print(f'Текущая температура {data.temp}')

class PressureView(Observer):
    def update(self, data):
        print(f'Текущее давление {data.press}')

class WetView(Observer):
    def update(self, data):
        print(f'Текущая влажность {data.wet}')

print('*'*20, ' Observer ', '*'*20)
subject = Subject()
tv = TemperatureView()
pr = PressureView()
wet = WetView()

subject.add_observer(tv)
subject.add_observer(pr)
subject.add_observer(wet)

subject.change_data(Data(23, 150, 83))
# выведет строчки:
# Текущая температура 23
# Текущее давление 150
# Текущая влажность 83
subject.remove_observer(wet)
subject.change_data(Data(24, 148, 80))
# выведет строчки:
# Текущая температура 24
# Текущее давление 148

# -----------------------------------------------

class Aircraft:
    def __init__(self, model, mass, speed, top):
        self._check_string(model)
        self._check_positive_num(mass)
        self._check_positive_num(speed)
        self._check_positive_num(top)

        self._model = model
        self._mass = mass
        self._speed = speed
        self._top = top

    def _check_string(self, string):
        if not isinstance(string, str):
            raise TypeError('неверный тип аргумента')
        
    def _check_positive_num(self, num):
        if not isinstance(num, (int, float)) or num <= 0:
            raise TypeError('неверный тип аргумента')
        
class PassengerAircraft(Aircraft):
    def __init__(self, model, mass, speed, top, chairs):
        super().__init__(model, mass, speed, top)
        self._check_positive_int(chairs)

        self._chairs = chairs
    
    def _check_positive_int(self, num):
        if not isinstance(num, int) or num <= 0:
            raise TypeError('неверный тип аргумента')

class WarPlane(Aircraft):
    def __init__(self, model, mass, speed, top, weapons):
        super().__init__(model, mass, speed, top)
        self._check_dict(weapons)

        self._weapons = weapons

    def _check_dict(self, dct):
        if not isinstance(dct, dict):
            raise TypeError('неверный тип аргумента')
        

print('*'*20, ' Aircraft ', '*'*20)

# PassengerAircraft: МС-21, 1250, 8000, 12000.5, 140
# PassengerAircraft: SuperJet, 1145, 8640, 11034, 80
# WarPlane: Миг-35, 7034, 25000, 2000, {"ракета": 4, "бомба": 10}
# WarPlane: Су-35, 7034, 34000, 2400, {"ракета": 4, "бомба": 7}

planes = [
    PassengerAircraft('МС-21', 1250, 8000, 12000.5, 140),
    PassengerAircraft('SuperJet', 1145, 8640, 11034, 80),
    WarPlane('Миг-35', 7034, 25000, 2000, {"ракета": 4, "бомба": 10}),
    WarPlane('Су-35', 7034, 34000, 2400, {"ракета": 4, "бомба": 7})
]

# -----------------------------------------------

vector_log = []   # наименование (vector_log) в программе не менять!

# def integer_params(cls):
#     methods = {k: v for k, v in cls.__dict__.items() if callable(v)}
#     for k, v in methods.items():
#         setattr(cls, k, integer_params_decorated(v))

#     return cls

def class_log(log_lst):
    def method_decorator(method):
        def wrapper(*args, **kwargs):
            log_lst.append(method.__name__)

            return method(*args, **kwargs)
        return wrapper

    def wrapper(cls):
        methods = {k: v for k, v in cls.__dict__.items() if callable(v)}
        for k, v in methods.items():
            setattr(cls, k, method_decorator(v))

        return cls
    
    return wrapper
    

@class_log(vector_log)
class Vector:
    def __init__(self, *args):
        self.__coords = list(args)

    def __getitem__(self, item):
        return self.__coords[item]

    def __setitem__(self, key, value):
        self.__coords[key] = value

print('*'*20, ' class_log ', '*'*20)
v = Vector(1, 2, 3)
v[0] = 10

print(vector_log)

# -----------------------------------------------

CURRENT_OS = 'windows'   # 'windows', 'linux'


class WindowsFileDialog:
    def __init__(self, title, path, exts):
        self.__title = title # заголовок диалогового окна
        self.__path = path  # начальный каталог с файлами
        self.__exts = exts  # кортеж из отображаемых расширений файлов


class LinuxFileDialog:
    def __init__(self, title, path, exts):
        self.__title = title # заголовок диалогового окна
        self.__path = path  # начальный каталог с файлами
        self.__exts = exts  # кортеж из отображаемых расширений файлов

class FileDialogFactory:
    def __new__(cls, *args, **kwargs):
        if CURRENT_OS == 'windows':
            return cls.create_windows_filedialog(*args, **kwargs)
        elif CURRENT_OS == 'linux':
            return cls.create_linux_filedialog(*args, **kwargs)

    @staticmethod
    def create_windows_filedialog(title, path, exts):
        return WindowsFileDialog(title, path, exts)

    @staticmethod
    def create_linux_filedialog(title, path, exts):
        return LinuxFileDialog(title, path, exts)


print('*'*20, ' FileDialogFactory ', '*'*20)

dlg = FileDialogFactory('Изображения', 'd:/images/', ('jpg', 'gif', 'bmp', 'png'))
print(dlg)