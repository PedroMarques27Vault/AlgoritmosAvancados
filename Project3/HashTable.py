import math
import sys


class HashTable:
    def __init__(self, _size,SIZE_FACTOR = None, method = 'PyHash', p = None):
        self.SIZE_FACTOR = SIZE_FACTOR
        if not SIZE_FACTOR:
            self.SIZE_FACTOR = 1.5

        self.method = method
        self.p = p
        if not p:
            self.p = 51

        self.size = math.ceil(_size * self.SIZE_FACTOR)
        self.structure = [None]*self.size
        self.keys = [None]*self.size

    def hash(self, key):

        if self.method == 'PyHash':
            key = hash(key)
        elif self.method == 'PRHF':
            key = sum([ord(key[i])*(self.p**i) for  i in range(len(key)) ])
        return key%self.size

    def put(self,key, value):

        _index = self.hash(key)
        self.structure[_index]=value
        self.keys[_index]=key

    def get(self,key):
        _index = self.hash(key)

        return self.structure[_index]

    def contains(self,key ):
        _index = self.hash(key)

        return self.keys[_index]!=None

    def length(self):
        return len([x for x in self.structure if x])

    def get_keys(self):
        return [x for x in self.keys if x]

    def get_values(self):
        return [self.structure[self.hash(k)] for k in self.get_keys()]

    def items(self):
        return [(k, self.structure[self.hash(k)]) for k in self.get_keys()]

