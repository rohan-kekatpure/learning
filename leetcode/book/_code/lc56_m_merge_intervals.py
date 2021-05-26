from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda x: x[0])
        merged = [intervals[0]]
        for left, right in intervals:
            if left > merged[-1][1]:
                merged.append([left, right])
            else:
                merged[-1][1] = max(right, merged[-1][1])
        return merged

