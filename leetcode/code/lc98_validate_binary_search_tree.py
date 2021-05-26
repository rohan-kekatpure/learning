# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def validate(self, node, minval, maxval):
        if (node.val <= minval) or (node.val >= maxval):
            return False

        validate_left = validate_right = True
        if node.left:
            validate_left = self.validate(node.left, minval, node.val)

        if node.right:
            validate_right = self.validate(node.right, node.val, maxval)

        return validate_left and validate_right

    def isValidBST(self, root: TreeNode) -> bool:
        return self.validate(root, float('-inf'), float('inf'))
