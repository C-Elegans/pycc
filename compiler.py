import parser,sys, codegen, peephole, transform
f = open(sys.argv[1],"r")
file =  f.read()
print file
ast = parser.parse(file)
print ast.pretty()
ast = transform.transform(ast)
print ast.pretty()
out = codegen.generate(ast)
out = peephole.optimize(out)
print out
o = open(sys.argv[2],"w")
o.write(out)

