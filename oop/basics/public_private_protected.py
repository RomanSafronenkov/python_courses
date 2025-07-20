class Clock:
    def __init__(self):
        self.__time = 0

    def set_time(self, tm):
        if self.check_time(tm):
            self.__time = tm

    def get_time(self):
        return self.__time

    @staticmethod
    def check_time(tm):
        if type(tm) == int and 0 <= tm < 100_000:
            return True
        return False


clock = Clock()
clock.set_time(4530)
print(clock.get_time())


# -----------------------------
class Money:
    def __init__(self, money):
        self.__money: int = 0
        self.set_money(money)

    def set_money(self, money):
        if self.__check_money(money):
            self.__money = money

    def get_money(self):
        return self.__money

    def add_money(self, mn):
        self.__money += mn.get_money()

    @staticmethod
    def __check_money(money):
        return type(money) == int and money >= 0


mn_1 = Money(10)
mn_2 = Money(20)
mn_1.set_money(100)
mn_2.add_money(mn_1)
m1 = mn_1.get_money()  # 100
m2 = mn_2.get_money()  # 120
print(m1, m2)


# -----------------------------
class Book:
    def __init__(self, author, title, price):
        self.__price = price
        self.__author = author
        self.__title = title

    def set_title(self, title):
        self.__title = title

    def set_author(self, author):
        self.__author = author

    def set_price(self, price):
        self.__price = price

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_price(self):
        return self.__price

# -----------------------------
class Line:
    def __init__(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2

    def set_coords(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2

    def get_coords(self):
        return self.__x1, self.__y1, self.__x2, self.__y2

    def draw(self):
        print(*[self.__x1, self.__y1, self.__x2, self.__y2])