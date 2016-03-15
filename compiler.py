import parser,sys, codegen, peephole
f = open(sys.argv[1],"r")
file =  f.read()
print file
ast = parser.parse(file)
print ast.pretty()
out = codegen.generate(ast)
out = peephole.optimize(out)
o = open(sys.argv[2],"w")
o.write(out)
o.write("""
mov rax, 0x2000001
mov rdi, 0
syscall
""")
