class Solution:
    def __init__(self):
        self.lca = None
        
    def func(self, node, p, q):
        if (not node) or self.lca:
            return False, False
        
        pl, ql = self.func(node.left, p, q)
        pr, qr = self.func(node.right, p, q)
        foundp = (node.val == p) or pl or pr
        foundq = (node.val == q) or ql or qr
        if foundp and foundq:
            if not self.lca:
                self.lca = node
        return foundp, foundq
    
    def lowestCommonAncestor(self, root, p, q):
        self.func(root, p.val, q.val)
        return self.lca
