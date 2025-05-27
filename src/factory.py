from template_generators import DSM5Generator, Nostradamus

def create_generator(type):
    if type=="dsm5":
        return DSM5Generator()
    elif type=="nostradamus":
        return Nostradamus()
