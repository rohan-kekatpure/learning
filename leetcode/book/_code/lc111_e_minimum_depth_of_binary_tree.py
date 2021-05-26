# Definition for a binary tree node.
from collections import deque
from typing import List

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def __init__(self):
        self.mindepth = 1000000

    def func(self, node, curr_depth):
        if node is None:
            return

        # Leafnode
        if (node.left is None) and (node.right is None):
            self.mindepth = min(curr_depth, self.mindepth)
            return

        if curr_depth > self.mindepth:
            return

        self.func(node.left, curr_depth + 1)
        self.func(node.right, curr_depth + 1)

    def minDepth(self, root: TreeNode) -> int:
        if root is None:
            return 0

        self.func(root, 1)
        return self.mindepth


class Solution2:
    def minDepth(self, root: TreeNode) -> int:
        """
        This problem naturally lends itself to a breadth-first search, since this way we avoid needlessly traversing any
        paths longer than the shortest path.
        """

        if not root:
            return 0

        queue = deque([(root, 1)])

        while queue:
            node, depth = queue.pop()
            if node.left and node.right:
                queue.appendleft((node.left, depth + 1))
                queue.appendleft((node.right, depth + 1))
            elif node.left:
                queue.appendleft((node.left, depth + 1))
            elif node.right:
                queue.appendleft((node.right, depth + 1))
            else:
                return depth
