class Animal:
    def __init__(self, name, old):
        self.name = name
        self.old = old

class Cat(Animal):
    def __init__(self, name, old, color, weight):
        super().__init__(name, old)
        self.color = color
        self.weight = weight

    def get_info(self):
        return f'{self.name}: {self.old}, {self.color}, {self.weight}'

class Dog(Animal):
    def __init__(self, name, old, breed, size):
        super().__init__(name, old)
        self.breed = breed
        self.size = size

    def get_info(self):
        return f'{self.name}: {self.old}, {self.breed}, {self.size}'
    

print('*'*20, ' Animal ', '*'*20)    
cat = Cat('кот', 4, 'black', 2.25)
print(cat.get_info())

# -----------------------------------------------

class Thing:
    NUM_PRODUCTS = 0

    def __new__(cls, *args, **kwargs):
        Thing.NUM_PRODUCTS += 1
        return super().__new__(cls)

    def __init__(self, name, price):
        self.id = self.NUM_PRODUCTS
        self.name = name
        self.price = price
        self.weight = None
        self.dims = None
        self.memory = None
        self.frm = None

    def get_data(self):
        return (self.id, 
                self.name, 
                self.price, 
                self.weight, 
                self.dims, 
                self.memory, 
                self.frm)

class Table(Thing):
    def __init__(self, name, price, weight, dims):
        super().__init__(name, price)
        self.weight = weight
        self.dims = dims

class ElBook(Thing):
    def __init__(self, name, price, memory, frm):
        super().__init__(name, price)
        self.memory = memory
        self.frm = frm

print('*'*20, ' Thing ', '*'*20)
table = Table("Круглый", 1024, 812.55, (700, 750, 700))
book = ElBook("Python ООП", 2000, 2048, 'pdf')

print(*table.get_data())
print(*book.get_data())

# -----------------------------------------------
class GenericView:
    def __init__(self, methods=('GET',)):
        self.methods = methods

    def get(self, request):
        return ""

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

class DetailView(GenericView):
    def __init__(self, methods=('GET', )):
        super().__init__(methods)

    def render_request(self, request, method):
        if not method in self.methods:
            raise TypeError('данный запрос не может быть выполнен')
        
        func = self.__getattribute__(method.lower())
        return func(request)

    def get(self, request):
        if not isinstance(request, dict):
            raise TypeError('request не является словарем')
        
        if not 'url' in request.keys():
            raise TypeError('request не содержит обязательного ключа url')
        
        return f"url: {request['url']}"
    
print('*'*20, ' DetailView ', '*'*20)
dv = DetailView()
html = dv.render_request({'url': 'https://site.ru/home'}, 'GET')   # url: https://site.ru/home
print(html)

# -----------------------------------------------
class Singleton:
    CREATED = None

    def __new__(cls, *args, **kwargs):
        if cls.CREATED is not None:
            return cls.CREATED
        
        obj = super().__new__(cls)
        cls.CREATED = obj
        return obj
    
    def __init__(self, name):
        if self.__dict__.get('name') is None:
            self.name = name
    
class Game(Singleton):
    def __init__(self, name):
        super().__init__(name)

print('*'*20, ' Game ', '*'*20)
game = Game('Fallout')
print(game, game.name)
game2 = Game('Origin')
print(game2, game2.name)

# -----------------------------------------------
class Validator:
    def _is_valid(self, data):
        return True

    def __call__(self, data):
        if self._is_valid(data):
            return data
        
        else:
            raise ValueError('данные не прошли валидацию')
        
class IntegerValidator(Validator):
    def __init__(self, min_value, max_value):
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value

    def _is_valid(self, data):
        if isinstance(data, int) and (self.min_value <= data <= self.max_value):
            return True
        return False


class FloatValidator(Validator):
    def __init__(self, min_value, max_value):
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value

    def _is_valid(self, data):
        if isinstance(data, float) and (self.min_value <= data <= self.max_value):
            return True
        return False
    
print('*'*20, ' Validator ', '*'*20)
integer_validator = IntegerValidator(-10, 10)
float_validator = FloatValidator(-1, 1)
res1 = integer_validator(10)  # исключение не генерируется (проверка проходит)
try:
    res2 = float_validator(10)    # исключение ValueError
except ValueError as e:
    print(e)

# -----------------------------------------------
class Layer:
    def __init__(self, name='Layer'):
        self.name = name
        self.next_layer = None

    def __call__(self, other):
        self.next_layer = other
        return other
    
class Input(Layer):
    def __init__(self, inputs):
        super().__init__('Input')
        self.inputs = inputs

class Dense(Layer):
    def __init__(self, inputs, outputs, activation):
        super().__init__('Dense')
        self.inputs = inputs
        self.outputs = outputs
        self.activation = activation

class NetworkIterator:
    def __init__(self, network):
        self.network = network
        self.cur = None

    def __iter__(self):
        self.cur = self.network
        return self
    
    def __next__(self):
        if self.cur is None:
            raise StopIteration()
        layer = self.cur
        self.cur = self.cur.next_layer
        return layer
        
print('*'*20, ' NeuralNetwork ', '*'*20)

network = Input(128)
layer = network(Dense(network.inputs, 1024, 'linear'))
layer = layer(Dense(layer.outputs, 10, 'softmax'))

for x in NetworkIterator(network):
    print(x.name)

# -----------------------------------------------
class Vector:
    def __init__(self, *args):
        self.__coords = args

    def get_coords(self):
        return tuple(self.__coords)
    
    def check_size(self, other):
        return len(self.get_coords()) == len(other.get_coords())
    
    def parse_output(self, coords):
        return Vector(*coords)
    
    def __add__(self, other):
        if not self.check_size(other):
            raise TypeError('размерности векторов не совпадают')
        
        new_coords = []
        for coord1, coord2 in zip(self.get_coords(), other.get_coords()):
            new_coords.append(coord1 + coord2)

        return self.parse_output(new_coords)

    def __sub__(self, other):
        if not self.check_size(other):
            raise TypeError('размерности векторов не совпадают')
        
        new_coords = []
        for coord1, coord2 in zip(self.get_coords(), other.get_coords()):
            new_coords.append(coord1 - coord2)

        return self.parse_output(new_coords)
    
class VectorInt(Vector):
    def __init__(self, *args):
        if any([not isinstance(c, int) for c in args]):
            raise ValueError('координаты должны быть целыми числами')

        super().__init__(*args)

    def parse_output(self, coords):
        if all([isinstance(c, int) for c in coords]):
            return VectorInt(*coords)
        return Vector(*coords)
    


    