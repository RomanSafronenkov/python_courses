class FuncCall:
    def __init__(self, func):
        self.n_calls = 0
        self.__fn = func

    def __call__(self, x, *args, **kwargs):
        self.n_calls += 1
        return self.__fn(x)


@FuncCall
def x_2(x):
    return x * x


print(x_2(2), x_2(3), x_2(5), x_2.n_calls)

# --------------------------
from random import randint


class RandomPassword:
    def __init__(self, psw_chars, min_length, max_length):
        self.psw_chars = psw_chars
        self.min_length = min_length
        self.max_length = max_length

    def __call__(self, *args, **kwargs):
        pswd_len = randint(self.min_length, self.max_length)
        pswd = ''
        for i in range(pswd_len):
            pswd += self.psw_chars[randint(0, len(self.psw_chars) - 1)]
        return pswd


min_length = 5
max_length = 20
psw_chars = "qwertyuiopasdfghjklzxcvbnm0123456789!@#$%&*"

rnd = RandomPassword(psw_chars, min_length, max_length)
lst_pass = [rnd() for _ in range(3)]
print(lst_pass)


# --------------------------
class ImageFileAcceptor:
    def __init__(self, extensions):
        self.extensions = extensions

    def __call__(self, filename, *args, **kwargs):
        if filename.split('.')[-1] in self.extensions:
            return True
        return False


filenames = ["boat.jpg", "web.png", "text.txt", "python.doc", "ava.jpg", "forest.jpeg", "eq_1.png", "eq_2.png"]
acceptor = ImageFileAcceptor(('jpg', 'bmp', 'jpeg'))
image_filenames = filter(acceptor, filenames)
print(list(image_filenames))  # ["boat.jpg", "ava.jpg", "forest.jpeg"]


# --------------------------
class LoginForm:
    def __init__(self, name, validators=None):
        self.name = name
        self.validators = validators
        self.login = ""
        self.password = ""

    def post(self, request):
        self.login = request.get('login', "")
        self.password = request.get('password', "")

    def is_validate(self):
        if not self.validators:
            return True

        for v in self.validators:
            if not v(self.login) or not v(self.password):
                return False

        return True


class LengthValidator:
    def __init__(self, min_length, max_length):
        self.min_length = min_length
        self.max_length = max_length

    def __call__(self, string, *args, **kwargs):
        return self.min_length <= len(string) <= self.max_length


class CharsValidator:
    def __init__(self, chars):
        self.chars = chars

    def __call__(self, string, *args, **kwargs):
        return len(set(string) - set(self.chars)) == 0


from string import ascii_lowercase, digits

lg = LoginForm("Вход на сайт", validators=[LengthValidator(3, 50), CharsValidator(ascii_lowercase + digits)])
lg.post({"login": "root", "password": "panda"})
if lg.is_validate():
    print("Дальнейшая обработка данных формы")


# --------------------------
class DigitRetrieve:
    def __call__(self, string, *args, **kwargs):
        if string.isdigit() or (string[0] == '-' and string[1:].isdigit()):
            return int(string)


dg = DigitRetrieve()

st = ["123", "abc", "-56.4", "0", "-5"]
digits = list(map(dg, st))  # [123, None, None, 0, -5]
print(digits)


# --------------------------
class RenderList:
    def __init__(self, type_list):
        self.type_list = 'ol' if type_list == 'ol' else 'ul'

    def __call__(self, lst, *args, **kwargs):
        string = f"<{self.type_list}>\n"
        for elem in lst:
            string += f'<li>{elem}</li>\n'
        string += f'</{self.type_list}>'
        return string


lst = ["Пункт меню 1", "Пункт меню 2", "Пункт меню 3"]
render = RenderList("ol")
html = render(lst)
print(html)


# --------------------------
class HandlerGET:
    def __init__(self, func):
        self.fn = func

    @staticmethod
    def get(func, request, *args, **kwargs):
        if request.get('method', None) in ['GET', None]:
            func_output = func(request)
            return f"GET: {func_output}"

    def __call__(self, request, *args, **kwargs):
        print("ВЫЗВАЛСЯ МЕТОД CALL")
        return self.get(self.fn, request, *args, **kwargs)


print('СОЗДАНИЕ ФУНКЦИИ')


@HandlerGET
def contact(request):
    return "Сергей Балакирев"


print(type(contact), 'ИСПОЛЬЗОВАНИЕ ФУНКЦИИ')
res = contact({"method": "GET", "url": "contact.html"})
print(res)


# --------------------------
class Handler:
    def __init__(self, methods=('GET',)):
        self.methods = methods

    def get(self, func, request, *args, **kwargs):
        return f"GET: {func(request)}"

    def post(self, func, request, *args, **kwargs):
        return f"POST: {func(request)}"

    def __call__(self, func):
        print("ВЫЗВАЛСЯ МЕТОД CALL")

        def wrapper(request, *args, **kwargs):
            method = request.get('method')
            method = 'GET' if method is None else method
            if method not in self.methods:
                return
            handler = self.__getattribute__(method.lower())
            return handler(func, request, *args, **kwargs)

        return wrapper


print('СОЗДАНИЕ ФУНКЦИИ')


@Handler(methods=('GET', 'POST'))  # по умолчанию methods = ('GET',)
def contact(request):
    return "Сергей Балакирев"


print(type(contact), 'ИСПОЛЬЗОВАНИЕ ФУНКЦИИ')
res = contact({"method": "POST", "url": "contact.html"})
print(res)
# --------------------------
class InputDigits:
    def __init__(self, func):
        self.fn = func

    def __call__(self, *args, **kwargs):
        string = self.fn()
        return list(map(int, string.split(' ')))

# input_dg = InputDigits(input)
# res = input_dg()
# print(res)

# --------------------------
class RenderDigit:
    def __call__(self, string, *args, **kwargs):
        try:
            return int(string)
        except ValueError:
            return None

class InputValues:
    def __init__(self, render):
        self.render = render

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            string = func()
            return list(map(self.render, string.split(' ')))
        return wrapper

input_dg = InputValues(render=RenderDigit())(input)
res = input_dg()
print(res)
