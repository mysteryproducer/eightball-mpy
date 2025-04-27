#from gen import Generator
import random

class DSM5Generator():#Generator):
    
    _conditions=list()
    _maxindex=0
    def __init__(self):
        with open('assets/dsm5.txt') as file:
            self._conditions=file.readlines()
        self._maxindex=len(self._conditions)-1
    
    def generate(self):
        ix=random.randint(0,self._maxindex)
        return self._conditions[ix].strip()