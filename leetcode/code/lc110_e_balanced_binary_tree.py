# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def __init__(self):
        self.bal = True

    def func(self, node, curr_height):
        if node is None:
            return curr_height

        if not self.bal:
            return 0

        left_height = self.func(node.left, 1 + curr_height)
        right_height = self.func(node.right, 1 + curr_height)
        if abs(left_height - right_height) > 1:
            self.bal = False
        return max(left_height, right_height)

    def isBalanced(self, root: TreeNode) -> bool:
        self.func(root, 0)
        return self.bal
