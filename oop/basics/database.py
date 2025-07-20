import sys

# программу не менять, только добавить два метода
lst_in = list(map(str.strip, sys.stdin.readlines()))  # считывание списка строк из входного потока


class DataBase:
    lst_data = []
    FIELDS = ('id', 'name', 'old', 'salary')

    # здесь добавлять методы
    def insert(self, data):
        for value in data:
            data_elem = {key: value for key, value in zip(self.FIELDS, value.split(' '))}
            self.lst_data.append(data_elem)

    def select(self, a, b):
        return self.lst_data[a:b+1]

print(lst_in)
db = DataBase()
db.insert(lst_in)
print(db.lst_data)
print(db.select(1, 5))