from typing import List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        # This is a BFS traversal of the binary tree
        frontier = [[root]]
        lo_traversal_vals = []
        while len(frontier) > 0:
            current_level_nodes = frontier.pop()
            current_level_vals = []
            next_level_nodes = []

            # For each node in current level we do:
            # 1. Extract its value into an array for current level
            # 2. Extract its children, if any, and populate next_level_nodes
            for node in current_level_nodes:

                # Extra check might be unnecessary
                if node is None:
                    continue

                    # Meat of the logic
                current_level_vals.append(node.val)
                left_child = node.left
                right_child = node.right
                if left_child:
                    next_level_nodes.append(left_child)
                if right_child:
                    next_level_nodes.append(right_child)

            if len(next_level_nodes) > 0:
                frontier.insert(0, next_level_nodes)

            if len(current_level_vals) > 0:
                lo_traversal_vals.append(current_level_vals)

        return lo_traversal_vals
