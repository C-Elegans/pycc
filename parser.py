from plyplus import Grammar
f = open("grammer.txt","r")
list_parser = Grammar(f.read())

r=list_parser.parse('int x = 1;')

print r


