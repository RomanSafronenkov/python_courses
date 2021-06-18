from abc import ABC, abstractmethod


class Base(ABC):
    def __init__(self, data, result):
        self.data = data
        self.result = result

    def get_answer(self):
        return [int(x >= 0.5) for x in self.data]

    @abstractmethod
    def get_score(self):
        pass

    @abstractmethod
    def get_loss(self):
        pass
