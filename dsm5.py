#from gen import Generator
import random

class DSM5Generator():#Generator):
    
    _conditions=list()
    _max=0
    def __init__(self):
        file = open('assets/dsm5.txt')
        self._conditions=file.read().split("\n")
        self._max=len(self._conditions)
    
    def generate(self):
        return self._conditions[random.randint(0,self._max)]