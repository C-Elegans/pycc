from plyplus import Grammar
f = open("grammer.txt","r")
list_parser = Grammar(f.read())

def parse(tokens):
    tokens = tokens.strip('\r\n\t')
    
    print tokens
    r=list_parser.parse(tokens)
    return r



