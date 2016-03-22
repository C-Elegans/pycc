from plyplus import *
def transform(tree):
    tree = TTransformer().transform(tree)
    return tree
    
class TTransformer(STransformer):
    if_id = 0
    def _if(self,tree):
        print tree.tail[0]
        id = strees.STree("id",[str(self.if_id)])
        self.if_id += 1
        beg= strees.STree("ifbegin",[id,tree.tail[0]])
        l = tree.tail[1:]
        l.insert(0,id)
        end=strees.STree("ifend",l)
        print end
        tree = strees.STree("statement",[beg,end])
        return tree
