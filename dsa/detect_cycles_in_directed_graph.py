from typing import Dict, Set
class CycleDetector:
    def _nodevisitor(self, v: int, adjacency_list: Dict, visited: Set , stack: Set) -> bool:
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

    def detect(self, adjacency_list: Dict):
        visited = set()
        for v in adjacency_list:
            stack = set()
            if not (v in visited):
                if self._nodevisitor(v, adjacency_list, visited, stack) == True:
                    return True

        return False

def main():
    adjacency_list = {
        1: [2, 3],
        2: [4, 5],
        3: [6, 7],
        4: [1],
        5: [],
        6: [],
        7: []
    }   

    cd = CycleDetector()
    print(cd.detect(adjacency_list))

if __name__ == '__main__':
    main()

