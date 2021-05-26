from typing import List
import numpy as np

class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        n1 = len(nums1)
        n2 = len(nums2)

        if n1 == n2 == 0:
            raise ValueError('both arrays empty')

        p = q = 0
        result = []
        while (p < n1) and (q < n2):
            if nums1[p] < nums2[q]:
                result.append(nums1[p])
                p += 1
            else:
                result.append(nums2[q])
                q += 1

        if p == n1:
            result.extend(nums2[q:])

        if q == n2:
            result.extend(nums1[p:])

        mid = (n1 + n2) // 2
        if (n1 + n2) % 2 == 0:
            return 0.5 * (result[mid] + result[mid - 1])
        else:
            return result[mid]

