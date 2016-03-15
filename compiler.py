import parser,sys, codegen
f = open(sys.argv[1],"r")
file =  f.read()
print file
ast = parser.parse(file)
print ast.pretty()
codegen.generate(ast)
