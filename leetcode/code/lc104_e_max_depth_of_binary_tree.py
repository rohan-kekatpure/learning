# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def helper(self, node, current_depth):
        d = current_depth

        if (node.left is None) and (node.right is None):
            return d

        left_depth = right_depth = d
        if node.left:
            left_depth = self.helper(node.left, d + 1)

        if node.right:
            right_depth = self.helper(node.right, d + 1)

        return max(left_depth, right_depth)

    def maxDepth(self, root: TreeNode) -> int:
        if root is None:
            return 0

        return self.helper(root, 1)

