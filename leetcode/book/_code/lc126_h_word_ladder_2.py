from typing import List
from heapq import heappush, heappop
from collections import defaultdict

class Solution1:
    """Solution based on adjacency matrix"""

    def dist(self, s, t):
        n = len(s)
        i = 0
        d = 0
        while i < n: 
            if s[i] != t[i]:
                d += 1
            i += 1
        return d

    def build_graph(self, wordList):
        n = len(wordList)
        g = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if self.dist(wordList[i], wordList[j]) == 1:
                    g[i][j] = g[j][i] = 1
        return g

    def findLaddersSearch(self, beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
        if beginWord == endWord:
            return [beginWord]

        if not (endWord in wordList):
            return []

        wordgraph = self.build_graph(wordList)
        visited = set()
        queue = []
        minlen = float('inf')
        paths = []

        # Initial population of queue
        n = len(wordList)
        for i in range(n):
            w = wordList[i]
            if self.dist(w, beginWord) == 1:
                heappush(queue, (1, [beginWord, w], i))

        while queue:
            pathlen, path, index = heappop(queue)

            if pathlen > minlen:
                break

            lastword = path[-1]            

            # Reached end
            if lastword == endWord:                
                if pathlen <= minlen:
                    minlen = pathlen
                    paths.append(path)
                    continue

            # If not reached end
            visited.add(lastword)
            neighbors = wordgraph[index]
            for i in range(n):
                if neighbors[i] == 1:
                    w = wordList[i]
                    if not (w in visited):
                        heappush(queue, (pathlen + 1, path + [w], i))

        return paths

    def findLaddersBidirectionalSearch(self, beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
        if beginWord == endWord:
            return [beginWord]

        if not (endWord in wordList):
            return []

        wordgraph = self.build_graph(wordList)
        visited = set()
        queue = []
        minlen = float('inf')
        paths = []

        # Initial population of queue
        n = len(wordList)
        for i in range(n):
            w = wordList[i]
            if self.dist(w, beginWord) == 1:
                heappush(queue, (1, [beginWord, w], i))

        while queue:
            pathlen, path, index = heappop(queue)

            if pathlen > minlen:
                break

            lastword = path[-1]            

            # Reached end
            if lastword == endWord:                
                if pathlen <= minlen:
                    minlen = pathlen
                    paths.append(path)
                    continue

            # If not reached end
            visited.add(lastword)
            neighbors = wordgraph[index]
            for i in range(n):
                if neighbors[i] == 1:
                    w = wordList[i]
                    if not (w in visited):
                        heappush(queue, (pathlen + 1, path + [w], i))

        return paths

        def findLadders(self, beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
            self.findLaddersSearch(beginWord, endWord, wordList)


class Solution2:
    """Solution based on adjacency list"""
    def dist(self, s, t):
        n = len(s)
        i = 0
        d = 0
        while i < n: 
            if s[i] != t[i]:
                d += 1
            i += 1
        return d

    def build_graph(self, wordList):        
        n = len(wordList)
        g = defaultdict(list)
        for i in range(n):
            for j in range(i + 1, n):
                if self.dist(wordList[i], wordList[j]) == 1:
                    g[wordList[i]].append(wordList[j])
                    g[wordList[j]].append(wordList[i])
        return g

    def findLadders(self, beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
        if beginWord == endWord:
            return [beginWord]

        if not (endWord in wordList):
            return []

        wordgraph = self.build_graph(wordList)
        visited = set()
        queue = []
        minlen = float('inf')
        paths = []

        # Initial population of queue
        n = len(wordList)
        for i in range(n):
            w = wordList[i]
            if self.dist(w, beginWord) == 1:
                heappush(queue, (1, [beginWord, w]))

        while queue:
            pathlen, path = heappop(queue)

            if pathlen > minlen:
                break

            lastword = path[-1]            

            # Reached end
            if lastword == endWord:                
                if pathlen <= minlen:
                    minlen = pathlen
                    paths.append(path)
                    continue

            # If not reached end
            visited.add(lastword)
            neighbors = wordgraph[lastword]
            for w in neighbors:
                if not (w in visited):
                    heappush(queue, (pathlen + 1, path + [w]))

        return paths


