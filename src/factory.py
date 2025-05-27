from dsm5 import DSM5Generator
from nostradamus import Nostradamus

def create_generator(type):
    if type=="dsm5":
        return DSM5Generator()
    elif type=="nostradamus":
        return Nostradamus()
