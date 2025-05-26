#Micropython doens't support abstract classes
#from abc import abstractmethod,ABCMeta
import random

punctuation="!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ "

class Generator():
#    @abstractmethod
    def generate():
        pass

class TemplateGenerator(Generator):

    def __init__(self,filename,zero_chance=.2):
        with open(filename) as file:
            self._conditions=file.readlines()
        self._conditions=filter(lambda s:((len(s.strip())>0) and not s.startswith('#')),self._conditions)
        self._conditions=map(lambda s:s.strip(),self._conditions)
        self._conditions=list(self._conditions)
        self._subs=dict()
        self._zero_chance=zero_chance
        self.prepare_subs()
        self._maxindex=len(self._conditions)-1
    
    def generate(self):
        ix=random.randint(0,self._maxindex)
        val=self._conditions[ix]
        val=self.substitute(val)
        return val

    def prepare_subs(self):
        all_subs=[x for x in self._conditions if x.startswith('[')]
        self._conditions=[x for x in self._conditions if not x.startswith('[')]
        for element in all_subs:
            b_ix=element.find(']')
            key=element[1:b_ix]
            value=element[b_ix+1:]
            sub_list=self._subs.get(key)
            if sub_list is None:
                sub_list=list()
                self._subs[key]=sub_list
            sub_list.append(value)

    def substitute(self,value):
        ob_ix=value.find('{')
        while ob_ix>=0:
            cb_ix=value.find('}')
            key=value[ob_ix+1:cb_ix]
            repl=self.get_sub(key)
            if repl!='':
                #
                if (ob_ix>0 and value[ob_ix-1]!=' '):
                    repl=' '+repl
                if cb_ix<(len(value)-1) and not ((value[cb_ix+1]==' ') or value[cb_ix+1] in punctuation):
                    repl=repl+' '
            value=value.replace('{'+key+'}',repl,1)
            ob_ix=value.find('{')
        return value

    def get_sub(self,key):
        #if the key is a selection (pipe-separated), pick one at random
        keys=key.split('|')
        if (len(keys)>1):
            key=keys[random.randrange(len(keys))]
        choices=self._subs[key]
        ix=random.randrange(len(choices))
#        print(str(ix)+","+str(len(choices)))
        choice=choices[random.randrange(len(choices))]
        return choice
