# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def __init__(self):
        self.paths = []
    
    def dfs(self, node, path):
        if (node.left is None) and (node.right is None):
            self.paths.append('->'.join(path + [str(node.val)]))
        
        v = str(node.val)
        if node.left:
            self.dfs(node.left, path + [v])
            
        if node.right:
            self.dfs(node.right, path + [v])
        
    def binaryTreePaths(self, root: TreeNode) -> List[str]:
        self.dfs(root, [])
        return self.paths
    