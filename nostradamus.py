#from gen import Generator
import random

class Nostradamus():#Generator):
    
    _conditions=list()
    _max=0
    def __init__(self):
        file = open('dsm5.txt')
        _conditions=file.read().split("\n")
        _max=len(_conditions)
    
    def generate(self):
        return _conditions[random.randint(0,_max)]