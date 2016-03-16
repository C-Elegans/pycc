import re
passes = []
passes.append((re.compile(r'push (.*)\npush (.*)\npop r(.*)\npop r(.*)',re.MULTILINE),r'mov r\3,\2\nmov r\4,\1'))
passes.append((re.compile(r'push (.*)\npop r(.*)',re.MULTILINE),r'mov r\2,\1'))
#passes.append((re.compile(r'push (.*)\lea (.*)\npop r(.*)',re.MULTILINE),r'mov \2\nmov r\3, \1'))
passes.append((re.compile(r'mov r(.*),r\1', re.MULTILINE),' '))
passes.append((re.compile(r'mov r(.*),(\d*)\nmov (.*),e\1', re.MULTILINE),r'mov DWORD PTR \3,\2'))
passes.append((re.compile(r'mov e(.*),(.*)\nmov r(.*),r\1\nmov (.*),e\3', re.MULTILINE),r'mov e\1,\2\nmov \4,e\1'))
print passes
def optimize(text):
    global passes
    for p in passes:
    
        text = re.sub(p[0],p[1],text)
        
    return text
