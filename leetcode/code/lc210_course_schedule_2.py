class Solution:
    def __init__(self):
        self.is_cyclic = False
                
    def dfs(self, v, graph, visited, path, stack):
        if self.is_cyclic:
            return
        
        visited.add(v)
        stack.add(v)
        for c in graph[v]:
            if not (c in visited):                                             
                self.dfs(c, graph, visited, path, stack)
            elif c in stack:
                self.is_cyclic = True                                                       
        path.append(v)
        stack.remove(v)
        
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        
        # Build adjacency list
        graph = {}
        prereqs = prerequisites
        for i in range(numCourses):
            graph[i] = []
            
        for child, parent in prereqs:
            graph[parent].append(child)
            
        # Get paths
        paths = []
        visited = set()                
        for v in graph:
            path = []
            stack = set()
            if not (v in visited):
                self.dfs(v, graph, visited, path, stack)
                paths.extend(path)
        return [] if self.is_cyclic else paths[::-1]

        
        
        
        