class Person:
    def __init__(self, fio, job, old, salary, year_job):
        self.fio = fio
        self.job = job
        self.old = old
        self.salary = salary
        self.year_job = year_job

        self._value = -1
        self._order = {
            0: 'fio',
            1: 'job',
            2: 'old',
            3: 'salary',
            4: 'year_job'
        }

    def __check_idx(self, idx):
        if idx not in list(range(5)):
            raise IndexError('неверный индекс')

    def __getitem__(self, item):
        self.__check_idx(item)
        key = self._order[item]
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__check_idx(key)
        key = self._order[key]
        self.__dict__[key] = value

    def __iter__(self):
        self._value = -1
        return self

    def __next__(self):
        while self._value != 4:
            self._value += 1
            key = self._order[self._value]
            return self.__dict__[key]
        else:
            raise StopIteration

pers = Person('Гейтс Б.', 'бизнесмен', 61, 1000000, 46)
pers[0] = 'Балакирев С.М.'
print(pers.fio)
for v in pers:
    print(v)
try:
    pers[5] = 123 # IndexError
except IndexError as e:
    print(e)

# ------------------------------------------------------

class Stack:
    def __init__(self):
        self.top = None
        self.n_elements = 0

        self._value = 0

    def push_back(self, obj):
        if not self.top:
            self.top = obj
            self.n_elements += 1
            return

        cur_elem = self.top
        while cur_elem.next:
            cur_elem = cur_elem.next

        cur_elem.next = obj
        self.n_elements += 1

    def push_front(self, obj):
        top = self.top
        self.top = obj
        self.top.next = top

        self.n_elements += 1

    def __getitem__(self, item):
        self.__check_idx(item)

        for i, elem in enumerate(self):
            if i == item:
                return elem.data

    def __setitem__(self, key, value):
        self.__check_idx(key)

        for i, elem in enumerate(self):
            if i == key:
                elem.data = value
                return

    def __iter__(self):
        self._value = -1
        return self

    def __next__(self):
        if self._value == -1:
            self._value += 1
            return self.top

        cur_elem = self.top
        while cur_elem:
            cur_elem = cur_elem.next
            self._value += 1
            if self._value == len(self):
                raise StopIteration
            return cur_elem

    def __len__(self):
        return self.n_elements

    def __check_idx(self, idx):
        if not (0 <= idx < len(self)):
            raise IndexError('неверный индекс')

    def __repr__(self):
        string = ""
        cur_elem = self.top
        while cur_elem:
            string += str(cur_elem) + '->'
            cur_elem = cur_elem.next
        return string[:-2]


class StackObj:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        return f'StackObj(data={self.data})'

st = Stack()
st.push_back(StackObj("1"))
st.push_front(StackObj("2"))
print(st)
print(len(st))
print(st[0], st[1])

assert st[0] == "2" and st[1] == "1", "неверные значения данных из объектов стека, при обращении к ним по индексу"

st[0] = "0"
assert st[0] == "0", "получено неверное значение из объекта стека, возможно, некорректно работает присваивание нового значения объекту стека"

for obj in st:
    assert isinstance(obj, StackObj), "при переборе стека через цикл должны возвращаться объекты класса StackObj"

try:
    a = st[3]
except IndexError:
    assert True
else:
    assert False, "не сгенерировалось исключение IndexError"