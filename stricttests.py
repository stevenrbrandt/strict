from strict import *

import math

class foo2:
    def __init__(self):
        self.a = 1
        self.b = 2

f = foo2()

@strict
def foo3():
    f.a = 1
foo3()

try:
    @strict
    def foo4():
        c += 1
    assert False
except UndefException:
    pass

@strict
def foo4():
    c = 0
    c += 1

try:
    @strict
    def foo6():
        print(math.sine(3))
    assert False
except UndefException:
    pass

@strict
def foo7():
    print(math.sin(3))

h = 1

@strict
def foo8():
    print(h)

try:
    @strict
    def foo9():
        print(h)
        h = 1
    assert False
except UndefException:
    pass
    
@strict
def foo10(a):
    if a > 1:
        b = 1
    else:
        b = 2
    b += 1
    
try:
    @strict
    def foo11(a):
        if a > 1:
            b = 1
        else:
            c = 2
        b += 1
    assert False
except UndefException:
    pass

try:
    @strict
    def foo12():
        for a in range(1,1):
            b = 0
        b += 1
        a += 1
    assert False
except UndefException:
    pass

@strict
def foo13():
    b = 0
    for a in range(1,1):
        b = 0
    b += 1
    a += 1

#@strict
#def foo(apple):
#    a = f.b
#    a += 1 + 2 * 3
#    if a < 3:
#        b = 1+h
#    else:
#        b = 2+h
#    b -= 1
#    s = {"a":1,"b":2}
#    q = 0
#    #q += 1
#    for q in range(10):
#        print(q)
#    print("hello")
#    def zap(u):
#        u += 1
#    class Noob(object):
#        pass
#    try:
#        math.sin(3)
#    except:
#        pass
#    if False:
#        raise Exception()
#    with open('/etc/group') as fi:
#        footxt = fi.read()
#foo(1)

#moo = 1

#@strict
#def moose(a):
#    if a > 2:
#        moo = 3

#print(moose.f.__code__.co_varnames)
