# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def __init__(self):
        self.found = False

    def func(self, node, tot, target):
        if node is None:
            return

        if node.left is None and node.right is None:
            if tot + node.val == target:
                self.found = True
            return

        if not self.found:
            self.func(node.left, tot + node.val, target)

        if not self.found:
            self.func(node.right, tot + node.val, target)

    def hasPathSum(self, root: TreeNode, targetSum: int) -> bool:
        self.func(root, 0, targetSum)
        return self.found
