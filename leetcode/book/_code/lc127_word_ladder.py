from typing import List
from heapq import heappush, heappop
from collections import defaultdict

from typing import List
from heapq import heappush, heappop
from collections import defaultdict

class Solution:
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

    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
        if beginWord == endWord:
            return 1

        if not (endWord in wordList):
            return 0

        wordgraph = self.build_graph(wordList)
        visited = set()
        queue = []
        paths = []

        # Initial population of queue
        n = len(wordList)
        for i in range(n):
            w = wordList[i]
            if self.dist(w, beginWord) == 1:
                heappush(queue, (1, [beginWord, w]))

        while queue:
            pathlen, path = heappop(queue)
            lastword = path[-1]            

            # Reached end
            if lastword == endWord:                
                return pathlen + 1

            # If not reached end
            visited.add(lastword)
            neighbors = wordgraph[lastword]
            for w in neighbors:
                if not (w in visited):
                    heappush(queue, (pathlen + 1, path + [w]))

        return 0

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

    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
        """Bidirectional search"""

        if (beginWord == endWord) or (not (endWord in wordList)):
            return 0

        wordgraph = self.build_graph(wordList)
        visited_fwd = {}
        visited_bck = {}
        queue_fwd = []
        queue_bck = []

        # Initial population of queue
        n = len(wordList)
        for w in wordList:
            if self.dist(w, beginWord) == 1:
                heappush(queue_fwd, (1, [beginWord, w]))

            if self.dist(w, endWord) == 1:
                heappush(queue_bck, (1, [endWord, w]))


        while queue_fwd or queue_bck:
            pathlen_fwd, path_fwd = heappop(queue_fwd)
            lastword_fwd = path_fwd[-1]            

            pathlen_bck, path_bck = heappop(queue_bck)
            lastword_bck = path_bck[-1]

            # Did the two frontiers meet?
            if lastword_fwd == lastword_bck:
                return pathlen_fwd + pathlen_bck

            # Check if lastword_fwd in visited_bck
            if lastword_fwd in visited_bck:
                return pathlen_fwd + visited_bck[lastword_fwd][0]

            # Check if lastword_bck in visited_fwd
            if lastword_bck in visited_fwd:
                return pathlen_bck + visited_fwd[lastword_bck][0]

            # # Check if lastword_fwd in queue_bck
            # for plbck, pth in queue_bck:
            #     if pth[-1] == lastword_fwd:
            #         return pathlen_fwd + plbck

            # # check if lastword_bck in queue_fwd
            # for plfwd, pth in queue_fwd:
            #     if pth[-1] == lastword_bck:
            #         return pathlen_bck + plfwd


            # Explore forward path
            visited_fwd[lastword_fwd] = (pathlen_fwd, path_fwd)
            neighbors_fwd = wordgraph[lastword_fwd]
            for w in neighbors_fwd:
                if not (w in visited_fwd):
                    heappush(queue_fwd, (pathlen_fwd + 1, path_fwd + [w]))

            # Explore backward path
            visited_bck[lastword_bck] = (pathlen_bck, path_bck)
            neighbors_bck = wordgraph[lastword_bck]
            for w in neighbors_bck:
                if not (w in visited_bck):
                    heappush(queue_bck, (pathlen_bck + 1, path_bck + [w]))


        return 0

