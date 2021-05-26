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
        yield from self.func(node.left)
        yield from self.func(node.right)
        yield node.val
    
    def postorderTraversal(self, root: TreeNode) -> List[int]:
        return list(self.func(root))