import math
import re


class CsurosCounterState:
    def __init__(self,d,x = 0, t=0,u=0):
        self.t = t
        self.u = u
        self.x = x
        self.d = d
        self.est_x = 0
        self.est_real = 0
    def increment(self):
        self.x+=1
        return self
    def __str__(self):
        return f'({self.d}:{self.x}:{self.t}:{self.u})'
    def increment_u(self):
        if self.u == ((2**self.d)):
            self.u = 0
        else:
            self.u +=1
        return self
    def estimate_x(self, d=0):
        self.est_x = (2**self.d) * self.t + self.u
        return self.est_x

    def estimate_real(self, d=0):
        m = 2**self.d
        self.est_real = (m+self.u)*(2**self.t) - m
        return self.est_real


