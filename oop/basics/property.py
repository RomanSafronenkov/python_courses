print('*****Car')
class Car:
    def __init__(self):
        self.__model = None

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, model):
        if type(model) == str and 2 <= len(model) <= 100:
            self.__model = model


car = Car()
car.model = 'Toyota'
print(car.model, car.__dict__)


# ---------------------------
print('*****WindowDlg')
class WindowDlg:
    def __init__(self, title, width, height):
        self.__title = title
        self.__width = width
        self.__height = height

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, width):
        if type(width) == int and 0 <= width <= 10000:
            self.__width = width
            self.show()

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height):
        if type(height) == int and 0 <= height <= 10000:
            self.__height = height
            self.show()

    def show(self):
        print(f"{self.__title}: {self.width}, {self.height}")

wdlg = WindowDlg('Bruh', 10, 20)
wdlg.width = 35
wdlg.height = 40

# ---------------------------
print('*****LinkedList')
class Stack:
    def __init__(self):
        self.top = None

    def push(self, obj):
        # if list is not empty
        if self.top:
            # set the pointer
            pointer = self.top
            while pointer.next:
                # get to the end of the list
                pointer = pointer.next
            # link the last object with one that is added
            pointer.next = obj
        else:
            # if list is empty just set the obj as first
            self.top = obj

    def pop(self):
        if not self.top:
            return None

        if self.top.next:
            # set the pointer
            pointer = self.top
            # if next.next is None then we got the one before the last
            while pointer.next.next:
                # get to the end of the list
                pointer = pointer.next
            # take the last
            obj = pointer.next
            # delete it from the list
            pointer.next = None
        else:
            # if list is empty just return the top and set it to None
            obj = self.top
            self.top = None
        return obj

    def get_data(self):
        data = []
        pointer = self.top
        # iterate through all linked list
        while pointer:
            data.append(pointer.data)
            pointer = pointer.next
        return data

class StackObj:
    def __init__(self, data):
        self.__data = data
        self.__next = None

    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, obj):
        if type(obj) in [type(self), type(None)]:
            self.__next = obj

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

st = Stack()
st.push(StackObj("obj1"))
st.push(StackObj("obj2"))
st.push(StackObj("obj3"))
res = st.get_data()    # ['obj1', 'obj2', 'obj3']
print(res)
print(st.pop().data)
res = st.get_data()    # ['obj1', 'obj2']
print(res)
st.push(StackObj("obj4"))
res = st.get_data()    # ['obj1', 'obj2', 'obj4']
print(res)
print(st.pop().data)
print(st.pop().data)
print(st.pop().data)
print(st.pop())
res = st.get_data()    # []
print(res)

# ---------------------------
class RadiusVector2D:
    MIN_COORD, MAX_COORD = -100, 1024

    def __init__(self, x=0, y=0):
        self.__x, self.__y = 0, 0
        if self.check_value(x) and self.check_value(y):
            self.__x = x
            self.__y = y

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        if self.check_value(x):
            self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        if self.check_value(y):
            self.__y = y

    @staticmethod
    def norm2(vector):
        return vector.x**2 + vector.y**2

    @classmethod
    def check_value(cls, value):
        return type(value) in [float, int] and cls.MIN_COORD <= value <= cls.MAX_COORD

# ---------------------------
