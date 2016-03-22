from peachpy import *
from peachpy.x86_64 import *
from plyplus import *
blockid = 0
out = ".text\n"
vars = ".intel_syntax noprefix\n.data\n"
current_function = None
functions = {}
global_vars= []
class Function():
    def __init__(self,name, ret):
        self.name = name
        self.variable_offsets = {}
        self.bp = 0
        self.returns = ret
    def add_var(self,name):
        self.variable_offsets[name] = self.bp+4
        self.bp += 4
    def __repr__(self):
        return str(self.name) +"->"+self.returns+" vars: "+ str(self.variable_offsets)+ " size: " + str(self.bp)
class VariableTransform(STransformer):
    def vardec(self,tree):
        if current_function:
            f=current_function
            name = tree.tail[0].tail[0]
            f.add_var(name)    
        return tree
    def assign(self,tree):
        if not current_function:
            global global_vars,out,vars
            
            name = tree.tail[0].tail[0].tail[0]
        
            global_vars +=name
            vars += "_%s: .int %d\n" %(name, int(tree.tail[1].tail[0].tail[0]))
        return tree
        
        
class VarGen(STransformer):
    def funcdef(self,tree):
        global current_function
        global functions
        
        current_function = Function(tree.tail[0].tail[0], tree.tail[1].tail[0])
        functions[current_function.name] = current_function
        tree = VariableTransform().transform(tree)
        sp_offset = 4
      
        return tree
def condition(cond):
    out =  "pop rbx\n"
    out += "pop rax\n"
    out += "xor rcx,rcx\n"
    out += "cmp rax,rbx\n"
    out += "set%s cl\n" % (cond)
    out += "push rcx\n"
    return out
class Expr(STransformer):
    
    def funcdef(self,tree):
        global out
        out += "mov rsp,rbp\npop rbp\nret\n"
    def number(self,tree):
        global out
        out += "push "+tree.tail[0]+"\n"
    def var(self,tree):
        global out
        varname = tree.tail[0].tail[0]
        if varname in current_function.variable_offsets:
            out += "mov eax,[rbp-"+str(current_function.variable_offsets[varname])+"]\n"
        elif varname in global_vars:
            out += "mov eax,[rip+_"+varname+"]\n"
        else:
            raise SyntaxError("No variable named "+varname)
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
        
        out += "call _" + tree.tail[0].tail[0] + "\n"
        out += "push rax\n"
    def eq(self,tree):
        global out
        out += condition("e")
    def gt(self,tree):
        global out
        out += condition("g")
    def lt(self,tree):
        global out
        out += condition("l")
    def le(self,tree):
        global out
        out += condition("le")  
    def ge(self,tree):
        global out
        out += condition("ge") 
    def block(self,tree):
        global out,blockid
        out += "block_%d_end:\n" % (blockid)
        blockid += 1
class CodeGen(STransformer):
    def assign(self, tree):
        global out,global_vars
        varname = tree.tail[0].tail[0].tail[0]
        if varname in current_function.variable_offsets:
            out += "pop rbx\n"
            out += "mov [rbp-"+str(current_function.variable_offsets[varname])+"],ebx\n"
        elif varname in global_vars:
            out += "pop rbx\n"
            out += "mov [rip+_"+varname+"],ebx\n"
        else:
            raise SyntaxError("No variable named "+varname)
        return tree
    def funcdef(self,tree):
        current_function =functions[tree.tail[0].tail[0]]
        global out
        out += "mov rsp,rbp\npop rbp\nret\n"
        return tree
    def func(self, tree):
        global out
        out += "call _" + tree.tail[0].tail[0] + "\n"
    def expr(self,tree):
        
        Expr().transform(tree)
        return tree
    def ret(self,tree):
        global out
        
        if current_function.returns != "void":
            out += "pop rax\n"
        else:
            raise ValueError("Cannot return from a void function")
    def ifbegin(self,tree):
        global out
        
        
        out += "//ifbegin\n"
        out += "if_begin_%s:\n" % (tree.tail[0].tail[0])
        out += "pop rax\n"
        out += "cmp eax,0\n"
        out += "je if_end_%s\n" % (tree.tail[0].tail[0])
    def ifend(self,tree):
        global out
        out += "//ifend\n"
        out += "if_end_%s:\n" % (tree.tail[0].tail[0])
    def whilebegin(self,tree):
        global out
        
        out += "//whilebegin\n"
        out += "while_begin_%s:\n" % (tree.tail[0].tail[0])
    def whiletest(self,tree):
        global out
        
        out += "//test\n"
        out += "pop rax\n"
        out += "cmp eax,0\n"
        out += "je while_end_%s\n" % (tree.tail[0].tail[0])
    def whileend(self,tree):
        global out
        out += "//whileend\n"
        out += "jmp while_begin_%s\n" % (tree.tail[0].tail[0])
        out += "while_end_%s:\n" % (tree.tail[0].tail[0])
        
def generate(ast):
    global out
    global in_function
    global current_function
    funcs = ast.select("funcdef")
    for func in funcs:
         print func
         VarGen().transform(func)
         ast.remove_kid_by_id(id(func))
    print functions
    print ast
    current_function = None
    VariableTransform().transform(ast)
    for func in funcs:
        print func
        
        fname = func.tail[0].tail[0]
        current_function = functions[fname]
        out += ".globl %s\n_%s:\n" % (fname,fname)
        out += "push rbp\nmov rbp,rsp\n"
        out += "sub rsp,"+str((current_function.bp+15)&~15) +"\n"
        
        CodeGen().transform(func)
    
   
    out += """
.globl start
start:
call _main
"""
    for var in global_vars:
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
    return vars+out
