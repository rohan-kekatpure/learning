from  typing import List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def func(self, left, right):
        if left > right:
            # We need the list to be nonempty since there
            # might be trees on the other side
            return [None]

        if left == right:
            return [TreeNode(left)]

        trees = []
        for i in range(left, right + 1):
            left_trees = self.func(left, i - 1)
            right_trees = self.func(i + 1, right)

            # Couple each left tree to each right
            # tree through the root node
            for lt in left_trees:
                for rt in right_trees:
                    root = TreeNode(i)
                    if lt:  # left tree can be null, only attach if present
                        root.left = lt
                    if rt:  # right tree can be null, only attach if present
                        root.right = rt
                    trees.append(root)
        return trees

    def generateTrees(self, n: int) -> List[TreeNode]:
        all_trees = self.func(1, n)
        return all_trees

def binaryTreeToList(root):
    arr = []

    def func(node):
        if node is None:
            arr.append(None)
            return

        arr.append(node.val)
        func(node.left)
        func(node.right)

    func(root)
    return arr[:-1]

def main():
    sol = Solution()
    trees = sol.generateTrees(3)
    from IPython import embed; embed(); exit(0)

if __name__ == '__main__':
    main()
