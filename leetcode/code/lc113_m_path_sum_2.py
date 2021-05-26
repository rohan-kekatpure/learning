from typing import List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def __init__(self):
        self.paths = []

    def func(self, node, tot, path, target):
        if node is None:
            return

        if node.left is None and node.right is None:
            if tot + node.val == target:
                self.paths.append(path + [node.val])
                return

        self.func(node.left, tot + node.val, path + [node.val], target)
        self.func(node.right, tot + node.val, path + [node.val], target)

    def pathSum(self, root: TreeNode, targetSum: int) -> List[List[int]]:
        self.func(root, 0, [], targetSum)
        return self.paths
