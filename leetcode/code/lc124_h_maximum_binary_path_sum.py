# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def __init__(self):
        self.maxsum = float('-inf')
        
    def func(self, node):
        if node is None:
            return 0
        leftsum = self.func(node.left)
        rightsum = self.func(node.right)
        nodesum = max(
            node.val, 
            node.val + leftsum, 
            node.val + rightsum, 
            node.val + leftsum + rightsum
        )
        
        self.maxsum = max(self.maxsum, nodesum)
        
        return max(
            node.val, 
            node.val + leftsum, 
            node.val + rightsum
        )
    
    def maxPathSum(self, root: TreeNode) -> int:
        self.func(root)
        return self.maxsum
