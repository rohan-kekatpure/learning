# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def __init__(self):
        self.vals = []
        
    def func(self, node, k):
        if len(self.vals) == k:
            return
        
        if node is None:
            return
        
        self.func(node.left, k)        
        self.vals.append(node.val)
        self.func(node.right, k)
            
    def kthSmallest(self, root: TreeNode, k: int) -> int:
        self.func(root, k)
        return self.vals[k - 1]