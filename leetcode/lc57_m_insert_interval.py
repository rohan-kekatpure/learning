from typing import List

class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        # Insertion
        intervals.append(newInterval)

        # Merging
        intervals.sort(key=lambda x: x[0])
        merged = [intervals[0]]
        for interval in intervals[1:]:
            left, right = interval
            end = merged[-1][1]
            if left > end:
                merged.append(interval)
            else:
                merged[-1][1] = max(end, right)
        return merged

def main():
    sol = Solution()
    intervals = [[1, 5]]
    newInterval = [2, 7]
    ans = sol.insert(intervals, newInterval)
    print(ans)

if __name__ == '__main__':
    main()
