from plyplus import *
from plyplus.strees import *
func_params = {}
def transform(tree):
    tree = TTransformer().transform(tree)
    functions = tree.select("funcdef")
    for func in functions:
        name = func.tail[0].tail[0]
        
        params = len(func.select("funcparams"))
        
        func_params[name] = params
    FunctionT().transform(tree)
    return tree
class FunctionT(STransformer):
    def func(self,tree):
    
        name = tree.tail[0].tail[0]
        params = len(tree.select("expr"))
        
        if not (name in func_params):
            raise SyntaxError("Function %s not defined" % (name))
        if params != func_params[name]:
            raise SyntaxError("Function %s expects %d parameter(s). Found: %d" % (name,func_params[name], params))
class SubExprRemover(STransformer):
    def expr(self,tree):
        print tree   
        return tree.tail[0]     
class TTransformer(STransformer):
    if_id = 0
    def _if(self,tree):
        
        id = strees.STree("id",[str(self.if_id)])
        self.if_id += 1
        beg= strees.STree("ifbegin",[id,tree.tail[0]])
        l = tree.tail[1:]
        l.insert(0,id)
        end=strees.STree("ifend",l)
       
        tree = strees.STree("statement",[beg,end])
        return tree
    def _while(self,tree):
        
        id = strees.STree("id",[str(self.if_id)])
        self.if_id += 1
        beg = strees.STree("whilebegin",[id])
        test= strees.STree("whiletest",[id,tree.tail[0]])
        l = tree.tail[1:]
        l.insert(0,id)
        end=strees.STree("whileend",l)
        
        tree = strees.STree("statement",[beg,test,end])
        return tree
    def _for(self,tree):
        id = strees.STree("id",[str(self.if_id)])
        beg = STree("whilebegin",[id])
        test =STree("whiletest",[id,tree.tail[1]])
        block = tree.tail[3]
        block.tail.append(STree("statement",[tree.tail[2]]))
        end = STree("whileend",[id,block])
        
        self.if_id += 1
        for t in tree.tail:
            print t.head
        tree = STree("block",[tree.tail[0],beg,test,end])
        
        return tree
    def expr(self,tree):
        if tree.select("func"):
            print tree
            print tree.select("func")
            print tree.tail[0]
            tree.tail[0].tail.append(STree("return_needed",[]))
        if tree.select("expr"):
            print tree.tail
            tree =SubExprRemover().transform(tree)
            
        return STree("expr",[tree])
