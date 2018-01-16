# strict
## Implement strict checking at (sort of) compile time for Python3

Normally, in Python, you can write code like the following

```
def print_apples(apples):
  if apples < 2:
    print("1 apple")
  else:
    print(aples,"apples")

print_apples(1)
```

It will run without any errors. The typo, where "aples" will
go unnoticed until someone calls print_apples(2). Wouldn't it
be nice to be able to detect this type of mistake? The strict
package does this for you:

```
from strict import *

@strict
def print_apples(apples):
  if apples < 2:
    print("1 apple")
  else:
    print(aples,"apples")

print_apples(1)
```

Now the program above will die with an UndefException. At
the time the decorator is applied, the Abstract Syntax
Tree (AST) for the function is generated and examined by
the decorator. If it finds symbols that are (at decorator
time) undefined, it will raise an exception.

Example 2:

```
verbose = True

def do_calculation(a,b):
    c = a + b

    if a + b > 100 and verbose:
        print("a+b=",c)
    if a + b == 0:
        verbose = False

do_calculation(1,1)
```

The problem here, of course, is that because of the assignment
of verbose when a+b==0, the other reference to verbose will not
be to the global. Our @strict decorator detects this, too.

Fixing the above code, either by getting rid of the explicit
setting of verbose, or by declaring verbose to be global, will
satisfy strict.

Example 3:

```
def option(a):
    if a == 0:
        b = 2
    else:
        c = 1
    b += 1
    return b

option(0)
```

As long as option is called with zero, no error will be detected.
Variable "b", however, will be undefined if we cal option(1).
The strict package will detect this error as well. However, if
we define variable b on all branches of the if statement, strict
will be satisfied.
```
from strict import *

@strict
def option(a):
    if a == 0:
        b = 2
    else:
        b = 1
    b += 1

option(0)
```
