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
        tree.head = "var"
        return tree
class Expr(STransformer):
    def number(self,tree):
        global out
        out += "push "+tree.tail[0]+"\n"
    def identifier(self,tree):
        global out
        out += "mov rax,[rip+_"+tree.tail[0]+"]\n"
        out += "push rax\n"
class CodeGen(STransformer):
    def assign(self, tree):
        global out
        print tree.tail
        out += "pop rbx\n"
        out += "lea rax,[rip+_"+tree.tail[0].tail[0].tail[0]+"]\n"
        out += "mov [rax],ebx\n"
        return tree
    def expr(self,tree):
        Expr().transform(tree)
        return tree

        
def generate(ast):
    global out
    ast = VariableTransform().transform(ast)
    print ast
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

