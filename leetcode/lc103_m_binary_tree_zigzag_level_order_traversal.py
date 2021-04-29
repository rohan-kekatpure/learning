from typing import List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def zigzagLevelOrder(self, root: TreeNode) -> List[List[int]]:
        if root is None:
            return []

        queue = [[root]]
        all_vals = []
        Z = 1
        while queue:
            level = queue.pop()
            next_level = []
            level_vals = []

            for node in level:
                level_vals.append(node.val)
                if node.left:
                    next_level.append(node.left)
                if node.right:
                    next_level.append(node.right)

            if len(next_level) > 0:
                queue.insert(0, next_level)

            if Z == -1:
                level_vals.reverse()

            all_vals.append(level_vals)

            Z *= -1

        return all_vals
