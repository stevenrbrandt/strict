# strict
Implement strict checking at (sort of) compile time for Python3

Normally, in Python, you can write code like the following

  def print_apples(apples):
    if apples < 2:
      print("1 apple")
    else:
      print(aples,"apples")

  print_apples(1)

It will run without any errors. The typo, where "aples" will
go unnoticed until someone calls print_apples(2). Wouldn't it
be nice to be able to detect this type of mistake? The strict
package does this for you:

  from strict import *
  
  @strict
  def print_apples(apples):
    if apples < 2:
      print("1 apple")
    else:
      print(aples,"apples")

  print_apples(1)

Now the program above will die with an UndefException.
