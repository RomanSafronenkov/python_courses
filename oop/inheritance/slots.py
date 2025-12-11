# -----------------------------------------------

class Person:
    __slots__ = ('_fio', '_old', '_job')

    def __init__(self, fio, old, job):
        self._fio = fio
        self._old = old
        self._job = job

print('*'*20, ' Person ', '*'*20)

persons = (
    Person('Суворов', 52, 'полководец'),
    Person("Рахманинов", 50, 'пианист, композитор'),
    Person('Балакирев', 34, 'программист и преподаватель'),
    Person('Пушкин', 32, 'поэт и писатель')
)

# -----------------------------------------------

class Planet:
    def __init__(self, name, diametr, period_solar, period):
        self._name = name
        self._diametr = diametr
        self._period_solar = period_solar
        self._period = period

class SolarSystem:
    __slots__ = (
        '_mercury',
        '_venus',
        '_earth',
        '_mars',
        '_jupiter',
        '_saturn',
        '_uranus',
        '_neptune'
    )

    _cls_obj = None

    def __new__(cls, *args, **kwargs):
        if cls._cls_obj:
            return cls._cls_obj
        
        obj = object.__new__(cls, *args, **kwargs)
        cls._cls_obj = obj
        return obj
    
    def __init__(self):
        self._mercury = Planet("Меркурий", 4878, 87.97, 1407.5)
        self._venus = Planet("Венера", 12104, 224.7, 5832.45)
        self._earth = Planet("Земля", 12756, 365.3, 23.93)
        self._mars = Planet("Марс", 6794, 687, 24.62)
        self._jupiter = Planet("Юпитер", 142800, 4340, 9.9)
        self._saturn = Planet("Сатурн", 120660, 10753, 10.63)
        self._uranus = Planet("Уран", 51118, 30665, 17.2)
        self._neptune = Planet("Нептун", 49528, 60150, 16.1)


print('*'*20, ' SolarSystem ', '*'*20)
s_system = SolarSystem()
print(id(s_system))

print(s_system._earth._diametr)

s_system2 = SolarSystem()
print(id(s_system2))

# -----------------------------------------------

class Star:
    __slots__ = (
        '_name',
        '_massa',
        '_temp'
    )

    def __init__(self, name, massa, temp):
        self._name = name
        self._massa = massa
        self._temp = temp


class WhiteDwarf(Star):
    __slots__ = (
        '_type_star',
        '_radius'
    )

    def __init__(self, name, massa, temp, type_star, radius):
        super().__init__(name, massa, temp)
        self._type_star = type_star
        self._radius = radius



class YellowDwarf(Star):
    __slots__ = (
        '_type_star',
        '_radius'
    )

    def __init__(self, name, massa, temp, type_star, radius):
        super().__init__(name, massa, temp)
        self._type_star = type_star
        self._radius = radius


class RedGiant(Star):
    __slots__ = (
        '_type_star',
        '_radius'
    )

    def __init__(self, name, massa, temp, type_star, radius):
        super().__init__(name, massa, temp)
        self._type_star = type_star
        self._radius = radius


class Pulsar(Star):
    __slots__ = (
        '_type_star',
        '_radius'
    )

    def __init__(self, name, massa, temp, type_star, radius):
        super().__init__(name, massa, temp)
        self._type_star = type_star
        self._radius = radius


print('*'*20, ' Stars ', '*'*20)

stars = [
    RedGiant('Альдебаран', 5, 3600, 'красный гигант', 45),
    WhiteDwarf('Сириус А', 2.1, 9250, 'белый карлик', 2),
    WhiteDwarf('Сириус B', 1, 8200, 'белый карлик', 0.01),
    YellowDwarf('Солнце', 1, 6000, 'желтый карлик', 1)
]

white_dwarfs = list(filter(lambda x: isinstance(x, WhiteDwarf), stars))
print(stars)
print(white_dwarfs)

# -----------------------------------------------

class Note:
    _allowed_notes = ('до', 'ре', 'ми', 'фа', 'соль', 'ля', 'си')

    def __init__(self, name, ton):
        self._name = name
        self._ton = ton

    def __setattr__(self, name, value):
        if name == '_name':
            if value not in self._allowed_notes:
                raise ValueError('недопустимое значение аргумента')
            
        elif name == '_ton':
            if value not in [-1, 0, 1]:
                raise ValueError('недопустимое значение аргумента')
            
        super.__setattr__(self, name, value)

class Notes:
    __slots__ = '_do', '_re', '_mi', '_fa', '_solt', '_la', '_si'
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self._do = Note('до', 0)
        self._re = Note('ре', 0)
        self._mi = Note('ми', 0)
        self._fa = Note('фа', 0)
        self._solt = Note('соль', 0)
        self._la = Note('ля', 0)
        self._si = Note('си', 0)

    def __getitem__(self, index):
        if index >= len(self.__slots__):
            raise IndexError('недопустимый индекс')
        
        name = self.__slots__[index]
        return super().__getattribute__(name)


print('*'*20, ' Note ', '*'*20)
note = Note('до', 0)

print(note._name, note._ton)

notes = Notes()
print(notes[0]._name)

# -----------------------------------------------

class Function:
    def __init__(self):
        self._amplitude = 1.0     # амплитуда функции
        self._bias = 0.0          # смещение функции по оси Oy

    def __call__(self, x, *args, **kwargs):
        return self._amplitude * self._get_function(x) + self._bias

    def _get_function(self, x):
        raise NotImplementedError('метод _get_function должен быть переопределен в дочернем классе')

    def __add__(self, other):
        if type(other) not in (int, float):
            raise TypeError('смещение должно быть числом')

        obj = self.__class__(self)
        obj._bias = self._bias + other
        return obj
    
    def __mul__(self, other):
        if type(other) not in (int, float):
            raise TypeError('масштаб быть числом')

        obj = self.__class__(self)
        obj._amplitude = self._amplitude * other
        return obj
    

class Linear(Function):
    def __init__(self, *args):
        super().__init__()

        if len(args) == 1 and isinstance(args[0], self.__class__):
            self.__dict__ = args[0].__dict__.copy()

        elif len(args) == 2:
            self._k = args[0]
            self._b = args[1]

    def _get_function(self, x):
        return self._k * x + self._b

print('*'*20, '  Function ', '*'*20)

f = Linear(1, 0.5)
f2 = f + 10   # изменение смещения (атрибут _bias)
y1 = f(0)     # 0.5
y2 = f2(0)    # 10.5
print(f._bias, f2._bias, y1, y2)

f = Linear(1, 0.5)
f2 = f * 5    # изменение амплитуды (атрибут _amplitude)
y1 = f(0)     # 0.5
y2 = f2(0)    # 2.5
print(f._amplitude, f2._amplitude, y1, y2)