from gen import TemplateGenerator

class DSM5Generator(TemplateGenerator):

    def __init__(self,zero_chance=.2):
        super().__init__('assets/dsm5.txt',zero_chance)
