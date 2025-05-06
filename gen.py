from abc import abstractmethod,ABCMeta

class Generator(metaclass=ABCMeta):
    @abstractmethod
    def generate():
        pass