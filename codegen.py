from peachpy import *
from peachpy.x86_64 import *
from plyplus import *
out = ".text\n.globl start\nstart:\n"
vars = ".intel_syntax noprefix\n.data\n"
var_names = []

class VariableTransform(STransformer):
    def vardec(self,tree):
        global vars
        var_names.append(tree.tail[0].tail[0])
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
    global out
    ast = VariableTransform().transform(ast)
    ast = CodeGen().transform(ast)
    for var in var_names:
        out += """
mov rax,2
lea rdi,[rip+printf_string]
mov rsi,'%c'
mov rdx,[rip+_%s]
call _printf
""" % (var,var)
    out += """
mov rax, 0x2000001
mov rdi, 0
syscall
"""
    out += 'printf_string: .asciz "%c: %d\\n"\n'
    print vars+out
    return vars+out
    
