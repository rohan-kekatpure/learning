# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def __init__(self):
        self.head = None
        self.curr_node = None

    def func(self, node):
        if node is None:
            return
        self.curr_node.right = TreeNode(node.val)
        self.curr_node = self.curr_node.right
        self.func(node.left)
        self.func(node.right)

    def flatten(self, root: TreeNode) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        if root is None:
            return

        self.head = self.curr_node = TreeNode()
        self.func(root)
        self.head = self.head.right
        root.left = None
        root.val = self.head.val
        root.right = self.head.right
