from typing import List


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> TreeNode:
        stack = []

        # Populate first element of stack
        n = len(postorder)
        root = TreeNode(postorder[n - 1])
        k = inorder.index(root.val)
        leftvals = inorder[:k]
        rightvals = inorder[k + 1:]
        stack.append((root, leftvals, 'L'))
        stack.append((root, rightvals, 'R'))
        i = n - 2

        # Loop
        while stack:
            parent, vals, side = stack.pop()

            if len(vals) == 0:
                continue

            head = TreeNode(postorder[i])
            i -= 1

            if side == 'L':
                parent.left = head
            else:
                parent.right = head

            k = vals.index(head.val)
            leftvals = vals[:k]
            rightvals = vals[k + 1:]
            stack.append((head, leftvals, 'L'))
            stack.append((head, rightvals, 'R'))

        return root
