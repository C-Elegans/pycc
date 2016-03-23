from plyplus import *
from plyplus.strees import *
def transform(tree):
    tree = TTransformer().transform(tree)
    return tree
    
class TTransformer(STransformer):
    if_id = 0
    def _if(self,tree):
        
        id = strees.STree("id",[str(self.if_id)])
        self.if_id += 1
        beg= strees.STree("ifbegin",[id,tree.tail[0]])
        l = tree.tail[1:]
        l.insert(0,id)
        end=strees.STree("ifend",l)
        print end
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
        print end
        tree = strees.STree("statement",[beg,test,end])
        return tree
    def _for(self,tree):
        id = strees.STree("id",[str(self.if_id)])
        beg = STree("whilebegin",[id])
        test =STree("whiletest",[id,tree.tail[1]])
        block = tree.tail[3]
        block.tail.append(STree("statement",[tree.tail[2]]))
        end = STree("whileend",[id,block])
        print block
        self.if_id += 1
        for t in tree.tail:
            print t.head
        tree = STree("block",[tree.tail[0],beg,test,end])
        
        return tree
    
