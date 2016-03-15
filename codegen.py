from peachpy import *
from peachpy.x86_64 import *
from plyplus import *
out = ".text\n.globl start\nstart:\n"
vars = ".intel_syntax noprefix\n.data\n"

class VariableTransform(STransformer):
    def vardec(self,tree):
        global vars
        vars += "_"+tree.tail[0].tail[0]+":\n"
        vars += ".int 0\n"
        return tree.tail[0]
class CodeGen(STransformer):
    def assign(self, tree):
        global out
        print "assign: " + str(tree.tail)
        out += "pop rax\n"
        out += "pop rbx\n"
        out += "mov [rbx],eax\n"
        return tree
    def identifier(self, tree):
        global out
        
        out += "lea rax,[rip+_"+tree.tail[0]+"]\n"
        out += "push rax\n"
        return tree
    def number(self, tree):
        global out
        out += "push " + tree.tail[0] +"\n"
        return tree
def generate(ast):
    ast = VariableTransform().transform(ast)
    ast = CodeGen().transform(ast)
    print vars+out
    return vars+out
    
