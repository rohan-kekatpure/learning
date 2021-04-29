class Solution:
    def __init__(self):
        self.vals = []
    def func(self, root):
        if not root:
            return
        
        yield root.val       
        yield from self.func(root.left)                     
        yield from self.func(root.right)
        
    def preorderTraversal(self, root: TreeNode) -> List[int]:
        return list(self.func(root))
