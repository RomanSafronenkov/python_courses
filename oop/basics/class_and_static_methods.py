from string import ascii_lowercase, digits

class CardCheck:
    CHARS_FOR_NAME = ascii_lowercase.upper() + digits

    @staticmethod
    def check_card_number(number):
        numbers = number.split('-')
        if len(numbers) != 4:
            return False

        if not all([num.isdigit() for num in numbers]):
            return False

        if not all([len(num) == 4 for num in numbers]):
            return False

        return True

    @classmethod
    def check_name(cls, name):
        names = name.split(' ')
        if len(names) != 2:
            return False

        name, surname = names
        if len(name) == 0 or len(surname) == 0:
            return False

        if len(set(name) - set(cls.CHARS_FOR_NAME)) != 0 or len(set(surname) - set(cls.CHARS_FOR_NAME)) != 0:
            return False

        return True

is_number = CardCheck.check_card_number("1234-5668-9012-0000")
is_name = CardCheck.check_name("SERGEI BALAKIREV")
print(is_number, is_name)

# --------------------------------------

class Video:
    def create(self, name):
        self.name = name

    def play(self):
        print(f"воспроизведение видео {self.name}")

class YouTube:
    videos = []

    @classmethod
    def add_video(cls, video):
        cls.videos.append(video)

    @classmethod
    def play(cls, video_indx):
        cls.videos[video_indx].play()

v1 = Video()
v2 = Video()
v1.create('Python')
v2.create('Python ООП')

YouTube.add_video(v1)
YouTube.add_video(v2)
YouTube.play(0)
YouTube.play(1)

# --------------------------------------
class AppStore:
    def __init__(self):
        self.apps = []

    def add_application(self, app):
        self.apps.append(app)

    def remove_application(self, app):
        del self.apps[self.apps.index(app)]

    @staticmethod
    def block_application(app):
        app.blocked = True

    def total_apps(self):
        return len(self.apps)

class Application:
    def __init__(self, name):
        self.name = name
        self.blocked = False

store = AppStore()
app_youtube = Application("Youtube")
store.add_application(app_youtube)
print(store.apps)
store.remove_application(app_youtube)
print(store.apps)

# --------------------------------------

class Viber:
    MESSAGES = []

    @classmethod
    def add_message(cls, msg):
        cls.MESSAGES.append(msg)

    @classmethod
    def remove_message(cls, msg):
        cls.MESSAGES.remove(msg)

    @staticmethod
    def set_like(msg):
        if msg.fl_like:
            msg.fl_like = False
        else:
            msg.fl_like = True

    @classmethod
    def show_last_message(cls, num):
        result = ""
        for msg in cls.MESSAGES[-num:]:
            result += msg.text + '\n'
        print(result)

    @classmethod
    def total_messages(cls):
        return len(cls.MESSAGES)

class Message:
    def __init__(self, text):
        self.text = text
        self.fl_like = False

msg = Message("Всем привет!")
Viber.add_message(msg)
Viber.add_message(Message("Это курс по Python ООП."))
Viber.add_message(Message("Что вы о нем думаете?"))
Viber.set_like(msg)
Viber.show_last_message(4)
Viber.remove_message(msg)
Viber.show_last_message(4)
print(True)