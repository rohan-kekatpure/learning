# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def helper(self, node: TreeNode, other: TreeNode) -> bool:
        # Base case
        if (node is None) and (other is None):
            return True

        if (node is None) or (other is None):
            return False

        # Check for values
        if node.val != other.val:
            return False

        # Child comparisons
        c1 = self.helper(node.left, other.right)
        c2 = self.helper(node.right, other.left)
        return c1 and c2

    def isSymmetric(self, root: TreeNode) -> bool:
        return self.helper(root.left, root.right)
