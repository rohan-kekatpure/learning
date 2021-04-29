# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def __init__(self):
        self.restored = False

    def func(self, node, min_node, max_node):
        if node is None:
            return

        if node.val < min_node.val:
            node.val, min_node.val = min_node.val, node.val
            self.restored = True
            return

        if node.val > max_node.val:
            node.val, max_node.val = max_node.val, node.val
            self.restored = True
            return

        if not self.restored:
            self.func(node.left, min_node, node)

        if not self.restored:
            self.func(node.right, node, max_node)

    def recoverTree(self, root: TreeNode) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        DMIN = TreeNode(val=-float('inf'))
        DMAX = TreeNode(val=float('inf'))
        self.func(root, DMIN, DMAX)
