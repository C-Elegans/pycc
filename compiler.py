import parser,sys, codegen, peephole, transform,preprocess
f = open(sys.argv[1],"r")
file =  f.read()

file = preprocess.process(file)
ast = parser.parse(file)

ast = transform.transform(ast)
print ast.pretty()
out = codegen.generate(ast)
out = peephole.optimize(out)
#print out
o = open(sys.argv[2],"w")
o.write(out)

