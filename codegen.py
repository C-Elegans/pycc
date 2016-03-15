from peachpy import *
from peachpy.x86_64 import *
from plyplus import *
out = "_start:\n"
vars = ""

class VariableTransform(STransformer):
    def vardec(self,tree):
        global vars
        vars += "_"+tree.tail[0].tail[0]+":\n"
        vars += ".int 0\n"
        return tree.tail[0]

def generate(ast):
    ast = gen_vars(ast)
    gen_recursive(ast)
    print vars+out
    
def gen_vars(ast):
    ast = VariableTransform().transform(ast)
    return ast
        
def gen_recursive(ast):
    global vars,out
    if type(ast) == strees.STree:
        for t in ast.tail:
            gen_recursive(t)

        if ast.head == 'assign':
            print "assign: " + str(ast.tail)
            out += "mov [rip+_"+ast.tail[0].tail[0] + "],"+ast.tail[1].tail[0]+"\n"
            
