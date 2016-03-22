import re
passes = []
passes.append((re.compile(r'([ \t]*)(.*)\+\+'),r'\1\2=\2+1'))
passes.append((re.compile(r'([ \t]*)(.*)--'),r'\1\2=\2-1'))
passes.append((re.compile(r'([ \t]*)(.*)(\+|-|\*|\/)=(.*)'),r'\1\2=\2\3\4'))
print passes
def process(text):
    global passes
    for p in passes:
    
        text = re.sub(p[0],p[1],text)
    print text  
    return text
        
    
