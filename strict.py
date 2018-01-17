#  Copyright (c) 2018 Steven R. Brandt
#
#  Distributed under the Boost Software License, Version 1.0. (See accompanying
#  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
import ast, re, inspect

class UndefException(Exception):
    def __init__(self,s):
        Exception.__init__(self,s)

class defined(object):
    def __init__(self,b):
        self.b = b
    def __str__(self):
        if self.b:
            return "Def"
        else:
            return "Udef"
        
Undefined = defined(False)
Defined   = defined(True)

def get_info(a,depth=0):
    "Print detailed information about an AST"
    nm = a.__class__.__name__
    print("  "*depth,end="")
    iter_children = True
    if nm == "Num":
        if type(a.n)==int:
            print("%s=%d" % (nm,a.n))
        else:
            print("%s=%f" % (nm,a.n))
    elif nm == "Global":
        print("Global:",dir(a))
    elif nm == "Str":
        print("%s='%s'" % (nm,a.s))
    elif nm == "Name":
        print("%s='%s'" %(nm,a.id))
    elif nm == "arg":
        print("%s='%s'" %(nm,a.arg))
    elif nm == "If":
        iter_children = False
        print(nm)
        get_info(a.test,depth)
        for n in a.body:
            get_info(n,depth+1)
        if len(a.orelse)>0:
            print("  "*depth,end="")
            print("Else")
            for n in a.orelse:
                get_info(n,depth+1)
    else:
        print(nm)
    for (f,v) in ast.iter_fields(a):
        if type(f) == str and type(v) == str:
            print("%s:attr[%s]=%s" % ("  "*(depth+1),f,v))
    if iter_children:
        for n in ast.iter_child_nodes(a):
            get_info(n,depth+1)

def dupdefs(d):
    "Create a copy of a dict"
    r = {}
    for k in d:
        r[k] = d[k]
    return r

builtins = {"long":1,"file":1}
for b in dir(globals()["__builtins__"]):
    builtins[b] = Defined

def getline(a):
    "Print out file and line information"
    fr = inspect.currentframe()
    while fr:
        line = fr.f_lineno
        fn = fr.f_code.co_filename
        fr = fr.f_back
    line += a.lineno
    return "%s:%d" % (fn,line)

def check_nm(n,defs,a,gl):
    "Check to see if a name is currently defined"
    if n in defs:
        if defs[n] == Defined:
            pass
        elif defs[n] == Undefined:
            raise UndefException("Undefined variable %s, line=%s" % (n,getline(a)))
    elif n in gl or n in builtins:
        pass
    else:
        raise UndefException("Undefined variable %s, line=%s" % (n,getline(a)))

depth = 0
def check_vars(a,defs,gl):
    "Check a class to see if it meets the strict definition"
    global depth
    nm = a.__class__.__name__
    if nm == "Str" or nm == "Num" or nm == "Lt" or nm == "Pass":
        return
    args = [arg for arg in ast.iter_child_nodes(a)]
    if nm == "Name":
        nm2 = args[0].__class__.__name__
        if nm2 == "Load":
            check_nm(a.id,defs,a,gl)
        elif nm2 == "Store":
            defs[a.id] = Defined
    elif nm == "FunctionDef":
        depth += 1
        if depth == 1:
            for arg in args:
                check_vars(arg,defs,gl)
        else:
            defs[a.name] = Defined
    elif nm == "BinOp" or nm == "Compare":
        check_vars(args[0],defs,gl)
        check_vars(args[2],defs,gl)
    elif nm == "Call":
        nm2 = args[0].__class__.__name__
        if nm2 == "Name":
            check_nm(args[0].id,defs,a,gl)
        elif nm2 == "Attribute":
            attr = args[0].attr
            args2 = [arg for arg in ast.iter_child_nodes(args[0])]
            nm3 = args2[0].__class__.__name__
            if nm3 == "Name":
                pkg_nm = args2[0].id
                if pkg_nm in gl or pkg_nm in locals():
                    pkg = gl[pkg_nm]
                    if not hasattr(pkg,attr):
                        raise UndefException("%s is not in %s, line=%s" % (attr,pkg_nm,getline(a)))
        for arg in args[1:]:
            check_vars(arg,defs,gl)
    elif nm == "Assign":
        nm2 = args[0].__class__.__name__
        if nm2 == "Name":
            defs[args[0].id] = Defined
        check_vars(args[1],defs,gl)
    elif nm == "Slice":
        print(nm,a.lower,a.upper,dir(a))
    elif nm == "AugAssign":
        check_nm(args[0].id,defs,a,gl)
        check_vars(args[2],defs,gl)
    elif nm == "For":
        d = dupdefs(defs)
        check_vars(args[0],defs,gl)
        for arg in args[1:]:
            check_vars(args[0],d,gl)
    elif nm == "While":
        d = dupdefs(defs)
        for arg in args:
            check_vars(args[0],d,gl)
    elif nm == "If":
        check_vars(a.test,defs,gl)
        d2 = dupdefs(defs)
        for b in a.body:
            check_vars(b,d2,gl)
        d3 = dupdefs(defs)
        for b in a.orelse:
            check_vars(b,d3,gl)
        for d in d2:
            if d in d3:
                if d2[d] == Defined and d3[d] == Defined:
                    defs[d] = Defined
    elif nm == "Attribute":
        if args[0].id in gl:
            obj = gl[args[0].id]
            if not hasattr(obj,a.attr):
                line = getline(a)
                raise UndefException("%s not in %s, line=%s" % (a.attr,args[0].id,line))
    elif nm == "arg":
        defs[a.arg] = Defined
    else:
       for arg in args:
           check_vars(arg,defs,gl)

def strict(f):
    gl = f.__globals__
    for b in dir(f.__globals__["__builtins__"]):
        builtins[b] = Defined

    # Get the source code
    src = inspect.getsource(f) #getsource(f)

    # Create the AST
    src = re.sub('^(?=\s+)','if True:\n',src)
    tree = ast.parse(src)
    defs = {}
    for v in f.__code__.co_varnames:
        defs[v] = Undefined
    check_vars(tree,defs,gl)
    return f
