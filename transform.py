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
    def _while(self,tree):
        print tree.tail[0]
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
    def inc(self,tree):
        print tree
        var = tree.tail[0]
        assign = strees.STree("assign",[var,strees.STree("expr",[strees.STree("add",[var,strees.STree("number",["1"])])])])
        print assign.pretty()
        return assign
    def dec(self,tree):
        print tree
        var = tree.tail[0]
        assign = strees.STree("assign",[var,strees.STree("expr",[strees.STree("sub",[var,strees.STree("number",["1"])])])])
        print assign.pretty()
        return assign
