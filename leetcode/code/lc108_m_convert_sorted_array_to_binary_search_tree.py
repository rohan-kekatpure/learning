from typing import List

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def func(self, parent, vals, side):
        if len(vals) == 0:
            return

        if len(vals) == 1:
            node = TreeNode(vals[0])
            if side == 'L':
                parent.left = node
            else:
                parent.right = node
            return

        n = len(vals)
        mid = n // 2
        head = TreeNode(vals[mid])
        if side == 'L':
            parent.left = head
        else:
            parent.right = head

        self.func(head, vals[:mid], 'L')
        self.func(head, vals[mid + 1:], 'R')

    def sortedArrayToBST(self, nums: List[int]) -> TreeNode:
        n = len(nums)
        mid = n // 2
        root = TreeNode(nums[mid])
        self.func(root, nums[:mid], 'L')
        self.func(root, nums[mid + 1:], 'R')
        return root
