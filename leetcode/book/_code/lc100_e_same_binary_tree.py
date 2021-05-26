class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def isSameTree(self, p: TreeNode, q: TreeNode) -> bool:
        # Only way to reach this base case is if
        # all comparisons so far have been true
        # and both trees have been exhausted
        if (not p) and (not q):
            return True

        if p and (not q):
            return False

        if (not p) and q:
            return False

        if p.val != q.val:
            return False

        return self.isSameTree(p.right, q.right) and self.isSameTree(p.left, q.left)

def build_tree_from_array(arr):
    n = len(arr)
    root = TreeNode(arr[0])
    if n == 1:
        return root

    queue = [root]
    i = 1
    while i < n - 1:
        node = queue.pop()
        node.left = TreeNode(arr[i])
        node.right = TreeNode(arr[i + 1])

        queue.insert(0, node.left)
        queue.insert(0, node.right)
        i += 2

    return root

