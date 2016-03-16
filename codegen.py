from peachpy import *
from peachpy.x86_64 import *
from plyplus import *
out = ".text\n"
vars = ".intel_syntax noprefix\n.data\n"
var_names = []
var_offsets = {}
sp_offset = 4
class VariableTransform(STransformer):
    def vardec(self,tree):
        global vars
        global sp_offset
        name = tree.tail[0].tail[0]
        var_names.append(name)
        var_offsets[name] = sp_offset
        sp_offset += 4
        tree.head = "var"
        return tree
class Expr(STransformer):
    def funcdef(self,tree):
        print "funcdef!",
        print tree
        global out
        out += "ret\n"
    def number(self,tree):
        global out
        out += "push "+tree.tail[0]+"\n"
    def var(self,tree):
        global out
        out += "mov eax,[rbp+"+str(var_offsets[tree.tail[0].tail[0]])+"]\n"
        out += "push rax\n"
    def add(self,tree):
        global out
        out += "pop rax\n"
        out += "pop rbx\n"
        out += "add rbx, rax\n"
        out += "push rbx\n"
    def sub(self,tree):
        global out
        out += "pop rax\n"
        out += "pop rbx\n"
        out += "sub rbx, rax\n"
        out += "push rbx\n"
    def mul(self, tree):
        global out
        out += "pop rax\n"
        out += "pop rbx\n"
        out += "imul eax,ebx\n"
        out += "push rax\n"
    def div(self,tree):
        global out
        out += "pop rbx\n"
        out += "pop rax\n"
        out += "xor rdx,rdx\n"
        out += "idiv rbx\n"
        out += "push rax\n"
class CodeGen(STransformer):
    def assign(self, tree):
        global out
        print tree.tail
        out += "pop rbx\n"
        
        out += "mov [rbp+"+str(var_offsets[tree.tail[0].tail[0].tail[0]])+"],ebx\n"
        return tree
    def expr(self,tree):
        Expr().transform(tree)
        return tree

        
def generate(ast):
    global out
    ast = VariableTransform().transform(ast)
    out += "sub rsp,"+str((sp_offset+15)&~15)+"\n"
    funcs = ast.select("funcdef")
    
    for func in funcs:
        print func
        fname = func.tail[1].tail[0]
        out += ".globl %s\n_%s:\n" % (fname,fname)
        Expr().transform(func)
    ast.remove_kids_by_head("funcdef")
    out += ".globl start\nstart:\nmov rbp,rsp\n"
    print ast
    ast = CodeGen().transform(ast)
    for var in var_names:
        out += """
        

mov rax,2
lea rdi,[rip+printf_string]
mov rsi,'%c'
mov rdx,[rbp+%s]
call _printf
""" % (var,var_offsets[var])
    out += """
mov rax, 0x2000001
mov rdi, 0
syscall
"""
    out += 'printf_string: .asciz "%c: %d\\n"\n'
    print vars+out
    return vars+out

