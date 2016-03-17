from peachpy import *
from peachpy.x86_64 import *
from plyplus import *
out = ".text\n"
vars = ".intel_syntax noprefix\n.data\n"
current_function = None
functions = {}

class Function():
    def __init__(self,name):
        self.name = name
        self.variable_offsets = {}
        self.bp = 0
    def add_var(self,name):
        self.variable_offsets[name] = self.bp+4
        self.bp += 4
    def __repr__(self):
        return str(self.name) +" vars: "+ str(self.variable_offsets)+ " size: " + str(self.bp)
class VariableTransform(STransformer):
    def vardec(self,tree):
        if current_function:
            f=current_function
            name = tree.tail[0].tail[0]
            f.add_var(name)
        return tree
        
class VarGen(STransformer):
    def funcdef(self,tree):
        global current_function
        global functions
        print "\n"
        print tree
        print "\n"
        current_function = Function(tree.tail[1].tail[0])
        functions[current_function.name] = current_function
        tree = VariableTransform().transform(tree)
        sp_offset = 4
      
        return tree
class Expr(STransformer):
    
    def funcdef(self,tree):
        global out
        out += "pop rbp\nret\n"
    def number(self,tree):
        global out
        out += "push "+tree.tail[0]+"\n"
    def var(self,tree):
        global out
    
        out += "mov eax,[rbp+"+str(current_function.variable_offsets[tree.tail[0].tail[0]])+"]\n"
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
    def func(self,tree):
        global out
        print tree
        out += "call _" + tree.tail[0].tail[0] + "\n"
        out += "push rax\n"
    def ret(self,tree):
        global out
        out += "pop rax\n"
        
class CodeGen(STransformer):
    def assign(self, tree):
        global out
        print tree.tail
        out += "pop rbx\n"
        out += "mov [rbp+"+str(current_function.variable_offsets[tree.tail[0].tail[0].tail[0]])+"],ebx\n"
        return tree
    def funcdef(self,tree):
        current_function =functions[tree.tail[1].tail[0]]
    def func(self, tree):
        global out
        out += "call _" + tree.tail[0].tail[0] + "\n"
        
    def expr(self,tree):
        Expr().transform(tree)
        return tree
    
    
        
def generate(ast):
    global out
    global in_function
    global current_function
    ast = VarGen().transform(ast)
    print ast
    current_function = Function("start")
    functions["start"] = current_function
    ast = VariableTransform().transform(ast)
    print ast
    funcs = ast.select("funcdef")
    print functions
    for func in funcs:
        print func
        
        fname = func.tail[1].tail[0]
        current_function = functions[fname]
        out += ".globl %s\n_%s:\n" % (fname,fname)
        out += "push rbp\nmov rbp,rsp\n"
        out += "sub rbp,"+str((current_function.bp+15)&~15) +"\n"
        
        Expr().transform(func)
    current_function =  functions["start"]
    ast.remove_kids_by_head("funcdef")
    out += ".globl start\nstart:\n"
    out += "sub rsp,"+str((current_function.bp+15)&~15)+"\nmov rbp,rsp\n"
    print ast
    ast = CodeGen().transform(ast)
    out += """
mov rax, 0x2000001
mov rdi, 0
syscall
"""
    out += 'printf_string: .asciz "%c: %d\\n"\n'
    print vars+out
    return vars+out
    

