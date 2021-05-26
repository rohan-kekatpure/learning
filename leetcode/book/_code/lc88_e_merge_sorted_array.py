from typing import List

class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        # move nums1 n elements to the right
        for i in range(m - 1, -1, -1):
            nums1[i + n] = nums1[i]

        # Now perform regular merge
        i = n
        j = 0
        k = 0
        while i < m + n and j < n:
            if nums1[i] < nums2[j]:
                nums1[k] = nums1[i]
                i += 1
            else:
                nums1[k] = nums2[j]
                j += 1
            k += 1

        while i < m + n:
            nums1[k] = nums1[i]
            i += 1
            k += 1

        while j < n:
            nums1[k] = nums2[j]
            j += 1
            k += 1

