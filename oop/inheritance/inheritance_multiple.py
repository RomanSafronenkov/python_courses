# -----------------------------------------------

class Digit:
    def __init__(self, value):
        if isinstance(value, (int, float)):
            self.value = value
        else:
            raise TypeError('значение не соответствует типу объекта')

class Integer(Digit):
    def __init__(self, value):
        if isinstance(value, int):
            super().__init__(value)
        else:
            raise TypeError('значение не соответствует типу объекта')

class Float(Digit):
    def __init__(self, value):
        if isinstance(value, float):
            super().__init__(value)
        else:
            raise TypeError('значение не соответствует типу объекта')
        
class Positive(Digit):
    def __init__(self, value):
        if isinstance(value, (float, int)) and value > 0:
            super().__init__(value)
        else:
            raise TypeError('значение не соответствует типу объекта')

class Negative(Digit):
    def __init__(self, value):
        if isinstance(value, (float, int)) and value < 0:
            super().__init__(value)
        else:
            raise TypeError('значение не соответствует типу объекта')

class PrimeNumber(Integer, Positive):
    def __init__(self, value):
        super().__init__(value)

class FloatPositive(Float, Positive):
    def __init__(self, value):
        super().__init__(value)


print('*'*20, ' Digits ', '*'*20)

digits = [
    PrimeNumber(3),
    PrimeNumber(33),
    PrimeNumber(333),
    FloatPositive(3.3),
    FloatPositive(33.3),
    FloatPositive(333.3),
    FloatPositive(3333.3),
    FloatPositive(33333.3),
]

lst_positive = list(filter(lambda x: isinstance(x, Positive), digits))
lst_float = list(filter(lambda x: isinstance(x, Float), digits))

print(lst_positive)
print(lst_float)
# print(Positive(-1))

# -----------------------------------------------

class ShopItem:
    ID_SHOP_ITEM = 0

    def __init__(self):
        super().__init__()
        ShopItem.ID_SHOP_ITEM += 1
        self._id = ShopItem.ID_SHOP_ITEM

    def get_pk(self):
        return self._id


class ShopGenericView:
    def __str__(self):
        args = self.__dict__
        return '\n'.join([f"{key}: {value}" for key, value in args.items()])


class ShopUserView:
    def __str__(self):
        args = self.__dict__
        return '\n'.join(
            [f"{key}: {value}" for key, value in args.items() if key != '_id']
            )


class Book(ShopItem, ShopUserView):
    def __init__(self, title, author, year):
        super().__init__()
        self._title = title
        self._author = author
        self._year = year

print('*'*20, ' ShopItem ', '*'*20)
book = Book("Python ООП", "Балакирев", 2022)
print(book)

# -----------------------------------------------

class RetriveMixin:
    def get(self, request):
        return "GET: " + request.get('url')


class CreateMixin:
    def post(self, request):
        return "POST: " + request.get('url')


class UpdateMixin:
    def put(self, request):
        return "PUT: " + request.get('url')
    
class GeneralView:
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')

    def render_request(self, request):

        if request.get('method') not in self.allowed_methods:
            raise TypeError(f"Метод {request.get('method')} не разрешен.")
        
        method_request = request.get('method').lower()  # имя метода, малыми буквами

        return getattr(self, method_request)(request)
    
class DetailView(RetriveMixin, GeneralView):
    allowed_methods = ('GET', 'PUT', )

print('*'*20, ' Mixin ', '*'*20)

view = DetailView()
html = view.render_request({'url': 'https://stepik.org/course/116336/', 'method': 'GET'})
print(html)   # GET: https://stepik.org/course/116336/

try:
    html = view.render_request({'url': 'https://stepik.org/course/116336/', 'method': 'PUT'})
except AttributeError as e:
    print(e)

class DetailView(RetriveMixin, UpdateMixin, GeneralView):
    allowed_methods = ('GET', 'PUT', )

view = DetailView()
html = view.render_request({'url': 'https://stepik.org/course/116336/', 'method': 'PUT'})
print(html)

# -----------------------------------------------

class Money:
    def __init__(self, value):
        self.__check_number(value)
        self._money = value

    def __check_number(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('сумма должна быть числом')

    @property
    def money(self):
        return self._money
    
    @money.setter
    def money(self, value):
        self.__check_number(value)
        self._money = value


class MoneyOperators:
    def __add__(self, other):
        if type(other) in (int, float):
            return self.__class__(self.money + other)

        if type(self) != type(other):
            raise TypeError('Разные типы объектов')

        return self.__class__(self.money + other.money)
    
    def __sub__(self, other):
        if type(other) in (int, float):
            return self.__class__(self.money - other)

        if type(self) != type(other):
            raise TypeError('Разные типы объектов')

        return self.__class__(self.money - other.money)
    

print('*'*20, ' Money ', '*'*20)

class MoneyR(Money, MoneyOperators):
    def __str__(self):
        return f"MoneyR: {self.money}"


class MoneyD(Money, MoneyOperators):
    def __str__(self):
        return f"MoneyD: {self.money}"
    
m1 = MoneyR(1)
m2 = MoneyD(2)
m = m1 + 10
print(m)  # MoneyR: 11
m = m1 - 5.4

print(m)
try:
    m = m1 + m2  # TypeError
except TypeError as e:
    print(e)