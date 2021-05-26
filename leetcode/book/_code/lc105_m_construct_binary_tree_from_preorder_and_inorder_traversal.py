from typing import List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> TreeNode:
        stack = []
        root = TreeNode(preorder[0])
        k = inorder.index(root.val)
        leftvals = inorder[:k]
        rightvals = inorder[k + 1:]
        stack.append((root, rightvals, 'R'))
        stack.append((root, leftvals, 'L'))
        i = 1
        while stack:
            parent, vals, side = stack.pop()

            if len(vals) == 0:
                continue

            headval = preorder[i]
            i += 1
            head = TreeNode(headval)
            if side == 'L':
                parent.left = head
            else:
                parent.right = head

            k = vals.index(headval)

            leftvals = vals[:k]
            rightvals = vals[k + 1:]
            stack.append((head, rightvals, 'R'))
            stack.append((head, leftvals, 'L'))

        return root
