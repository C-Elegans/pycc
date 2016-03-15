from peachpy import *
from peachpy.x86_64 import *
from plyplus import *
def generate(ast):
    gen_recursive(ast)
def gen_recursive(ast):
    print ast
    if type(ast) == strees.STree:
        for t in ast.tail:
            gen_recursive(t)
        
        if ast.head == 'assign':
            print "assign" + str(ast.tail)
    
