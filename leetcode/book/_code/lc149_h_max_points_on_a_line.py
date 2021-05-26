from typing import List
from collections import defaultdict
import math

class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        if n == 1: return 1
        lines = defaultdict(int)
        for i in range(n):
            xi, yi = points[i]
            for j in range(i + 1, n):
                xj, yj = points[j]

                # Vertical line
                if xi == xj:
                    m = 'inf'
                    c = xi
                    lines[(m, c)] += 1
                    continue

                # Regular lines
                m = (yj - yi) / (xj - xi)
                c = yj - m * xj

                # Matching with existing lines
                matched = False
                tol = 1.0e-6
                for ml, cl in lines.keys():
                    if ml == 'inf': continue
                    if (abs(ml - m) < tol) and (abs(cl - c) < tol):
                        lines[(ml, cl)] += 1
                        matched = True

                # Create new line
                if not matched:
                    lines[(m, c)] += 1

        # The counter at each value is V = k(k-1)/2 where
        # k is the number of points on that line. To retrieve
        # the number of points, we have to solve a quadratic.
        V = max(lines.values())
        numpoints = 0.5 * (1 + math.sqrt(1 + 8 * V))
        return int(math.floor(numpoints))

