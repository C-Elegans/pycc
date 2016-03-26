import os,subprocess
from joblib import Parallel, delayed
def compile_test(file):
    name = os.path.splitext(file)[0]
    print name
    os.system("python compiler.py test/%s.c test/%s.s"%(name,name))
    os.system("as -c test/%s.s -o test/%s.o"%(name,name))
    os.system("ld -lc test/%s.o -o test/%s.oo"%(name,name))
def run(file):
    name = os.path.splitext(file)[0]
    
    p = subprocess.Popen("test/"+name+".oo", stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = p.stdout.read()
    print output
    return output
    
def run_test(test_name):
    tokens = test_name.split()
    if tokens:
        print tokens[0]
        compile_test(tokens[0])
        o=run(tokens[0])
        output = o.splitlines()
        if len(tokens) != len(output) + 1:
            raise ValueError("output does not match test case")
        for i,line in enumerate(output):
            
            if tokens[i+1] != line:
                raise ValueError("output does not match test case")
    name = os.path.splitext(tokens[0])[0]
    os.system("rm test/%s.s"%(name))
    
    
tests = open("tests.list","r").readlines()

Parallel(n_jobs=len(tests))(delayed(run_test)(line) for line in tests)
    
print "All %d tests passed!" % (len(tests))
        

    
    
