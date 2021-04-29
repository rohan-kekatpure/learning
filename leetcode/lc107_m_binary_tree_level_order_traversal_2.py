from typing import List

# Definition for a binary tree node.

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def levelOrderBottom(self, root: TreeNode) -> List[List[int]]:
        level = [root]
        allvals = []
        while level:
            nextlevel = []
            vals = []
            for node in level:
                if not node: continue
                vals.append(node.val)
                nextlevel.append(node.left)
                nextlevel.append(node.right)

            if len(vals) > 0:
                allvals.append(vals)

            level = nextlevel if len(nextlevel) > 0 else None

        allvals.reverse()
        return allvals
