class Solution:
    def _nodevisitor(self, v, adjacency_list, visited, stack):
        visited.add(v)
        stack.add(v)

        for nbr in adjacency_list[v]:
            if not (nbr in visited):
                if self._nodevisitor(nbr, adjacency_list, visited, stack) == True:
                    return True
            elif nbr in stack:
                return True

        stack.remove(v)
        return False

    def isCyclic(self, adjacency_list):
        visited = set()
        for v in adjacency_list:
            stack = set()
            if not (v in visited):
                if self._nodevisitor(v, adjacency_list, visited, stack) == True:
                    return True

        return False
        
    
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        prereqs = prerequisites
        adjacency_list = defaultdict(list)
                
        for child, parent in prereqs:
            adjacency_list[child].append(parent)
            if not (parent in adjacency_list):
                adjacency_list[parent] = []
        
        return not self.isCyclic(adjacency_list)
            
        
            