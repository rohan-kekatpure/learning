"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

class Solution:
    def cloneGraph(self, node: 'Node') -> 'Node':
        """
        Approach:
        
        Serialize into an explicit adjacency list and build new.
        """

        if node is None:
            return
        
        head = node
        # BFS for serialization
        queue = [head]
        adjlist = {}
        visited = set()
        while queue:
            node = queue.pop()
            nbrs = [nb.val for nb in node.neighbors]
            adjlist[node.val] = nbrs
            for nb in node.neighbors:
                if not (nb.val in visited):
                    queue.insert(0, nb)
            visited.add(node.val)
        
        newnodes = {}
        for k in adjlist:
            newnodes[k] = Node(k, [])
        
        for k, nbidx in adjlist.items():
            nbrs = [newnodes[i] for i in nbidx]
            newnodes[k].neighbors = nbrs
        
        return newnodes[1]
                