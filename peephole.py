import re
passes = []
passes.append((re.compile(r'push (.*)\npop r(.*)',re.MULTILINE),r'mov r\2,\1'))
#passes.append((re.compile(r'push (.*)\nmov (.*)\npop r(.*)',re.MULTILINE),r'mov \2\nmov r\3, \1'))

print passes
def optimize(text):
    global passes
    for p in passes:
    
        text = re.sub(p[0],p[1],text)
        
    print text
    return text
