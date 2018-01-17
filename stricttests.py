#  Copyright (c) 2018 Steven R. Brandt
#
#  Distributed under the Boost Software License, Version 1.0. (See accompanying
#  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

# To run these tests, simply run "python3 stricttests.py". There should be no output.

from strict import *

import math

@strict
def foo1(a):
    a += 1

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

try:
    @strict
    def foo14(apple):
        if apple < 2:
            print(aple)
        else:
            print("Otherwise")
    assert False
except UndefException:
    pass

@strict
def foo15():
    def shark():
        pass
    shark()
