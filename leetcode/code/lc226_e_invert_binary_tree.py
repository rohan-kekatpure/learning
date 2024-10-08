# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def func(self, node):
        if node is None:
            return
        
        if (node.left is None) and (node.right is None):
            return
        
        node.left, node.right = node.right, node.left
        
        if node.left:
            self.func(node.left)
        if node.right:
            self.func(node.right)
            
    def invertTree(self, root: TreeNode) -> TreeNode:
        self.func(root)
        return root