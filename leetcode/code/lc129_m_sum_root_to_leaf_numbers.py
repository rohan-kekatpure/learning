# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def __init__(self):
        self.sum = 0
        
    def func(self, node, digits):
        if node is None:
            return
        
        # Words 'leaf node' should remind you to check
        # node.left and node.right        
        if (node.left is None) and (node.right is None):
            digits = digits + [node.val]
            num = int(''.join(str(d) for d in digits))
            self.sum += num
            return
        
        self.func(node.left, digits + [node.val])                
        self.func(node.right, digits + [node.val])
        
    def sumNumbers(self, root: TreeNode) -> int:
        self.func(root, [])
        return self.sum