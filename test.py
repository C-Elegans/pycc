import os,subprocess
def compile_test(file):
    name = os.path.splitext(file)[0]
    print name
    os.system("python compiler.py test/%s.c test/%s.s"%(name,name))
    os.system("as -c test/%s.s -o test/%s.o"%(name,name))
    os.system("ld -lc test/%s.o -o test/%s"%(name,name))
def run(file):
    name = os.path.splitext(file)[0]
    
    p = subprocess.Popen("test/"+name, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print p.stdout.readlines()
    output = p.wait()
    print p.stdout.readlines()
    print output
    return output
tests = open("tests.list","r").readlines()
for line in tests:

    tokens = line.split()
    if tokens:
        print tokens[0]
        compile_test(tokens[0])
        o=run(tokens[0])
        print type(o)

    
    
