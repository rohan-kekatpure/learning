# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class BSTIterator:

    def func(self, node):
        if node.left:
            yield from self.func(node.left)
        
        yield node.val
    
        if node.right:
            yield from self.func(node.right)
        
    def __init__(self, root: TreeNode):
        self.generator = self.func(root)
        self.nextval = next(self.generator)
        
    def next(self) -> int:
        if not (self.nextval is None):
            retval = self.nextval
            try:
                self.nextval = next(self.generator)
            except StopIteration:
                self.nextval = None
            return retval
        

    def hasNext(self) -> bool:
        return not (self.nextval is None)


# Your BSTIterator object will be instantiated and called as such:
# obj = BSTIterator(root)
# param_1 = obj.next()
# param_2 = obj.hasNext()