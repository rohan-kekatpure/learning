from typing import List
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def __init__(self):
        self.nodes = []

    def _inorderTraversal(self, node:TreeNode):
        if node is None:
            return
        self._inorderTraversal(node.left)
        self.nodes.append(node.val)
        self._inorderTraversal(node.right)

    def inorderTraversal(self, root: TreeNode) -> List[int]:
        self._inorderTraversal(root)
        return self.nodes

    def inorderTraversalIterative(self, root: TreeNode):
        stack = [root]
        vals = []
        while stack:
            node = stack.pop()
            stack.append(node.left)
            stack.append(node)
            stack.append(node.right)
            if node is None:
                continue

