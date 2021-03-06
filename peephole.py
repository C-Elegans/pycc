import re
passes = []
passes.append((re.compile(r'push (.*)\npush (.*)\npop r(.*)\npop r(.*)',re.MULTILINE),r'mov r\4,\1\nmov r\3,\2'))
passes.append((re.compile(r'push (.*)\npop r(.*)',re.MULTILINE),r'mov r\2,\1'))
#passes.append((re.compile(r'push (.*)\lea (.*)\npop r(.*)',re.MULTILINE),r'mov \2\nmov r\3, \1'))
passes.append((re.compile(r'mov r(.*),r\1\n', re.MULTILINE),''))
passes.append((re.compile(r'mov r(.*),(\d*)\nmov (.*),e\1', re.MULTILINE),r'mov DWORD PTR \3,\2'))
passes.append((re.compile(r'mov e(.*),(.*)\nmov r(.*),r\1\nmov (.*),e\3', re.MULTILINE),r'mov e\1,\2\nmov \4,e\1'))
passes.append((re.compile(r'mov r(.*),[r|e](.*)\nmov (.*),e\1', re.MULTILINE),r'mov \3,e\2'))
passes.append((re.compile(r'(sub|add) r(.*),0\n'),''))
passes.append((re.compile(r'mov r(.*),0'),r'xor r\1,r\1'))
passes.append((re.compile(r'mov e(.*),\[(.*)\]\nmov r(.*),r\1', re.MULTILINE),r'mov e\3,[\2]'))
passes.append((re.compile(r'mov r(.*),(\d)\n(add|sub|and|or) r(.*), r\1', re.MULTILINE),r'\3 r\4,\2'))
passes.append((re.compile(r'mov e(.*),\[(.*)\]\n(add|sub|and|or) r\1,(.*)\nmov \[\2\],e\1', re.MULTILINE),r'\3 DWORD PTR [\2],\4'))
passes.append((re.compile(r'mov r(.*),r(.*)\ncmp e\1,(.*)', re.MULTILINE),r'cmp e\2,\3'))
passes.append((re.compile(r'xor rcx,rcx\ncmp (.*),(.*)\nset(.*) cl\ncmp ecx,0\nje (.*)', re.MULTILINE),r'cmp \1,\2\nj\3 \4 //reverse'))

print passes
conditionsdict = {"l":"ge","g":"le","e":"ne","ne":"e","le":"g","ge":"l"}
condreverse = re.compile(r'j(.*) (.*)[ ]+//reverse')
def optimize(text):
    global passes
    for p in passes:
    
        text = re.sub(p[0],p[1],text)
    lines = text.splitlines()
    for i,s in enumerate(lines):
        match = condreverse.match(s)
        print s
        if match:
            cond =  conditionsdict[match.group(1)]
            target = match.group(2)
            lines[i] = "j%s %s" % (cond,target)
            
    return "\n".join(lines)
