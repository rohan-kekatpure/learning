from typing import List

class Solution:
    def find_closest_elem(self, list_, num):
        n = len(list_)
        left = 0
        right = n - 1
        mid = (left + right) // 2
        while left < right:
            mid = (left + right) // 2
            emid = list_[mid]
            if num == emid:
                return num

            if num > emid:
                left = mid + 1
            elif num < emid:
                right = mid - 1

        if abs(list_[mid] - num) < abs(list_[right] - num):
            return list_[mid]
        else:
            return list_[right]

    def find_closest(self, arr, num, k):
        n = len(arr)
        left = 0
        right = n - 1
        mid = (left + right) // 2
        while left < right:
            mid = (left + right) // 2
            i, j, val = arr[mid]
            if num == val:
                return num

            if num > val:
                left = mid + 1
            elif num < val:
                right = mid - 1

        if abs(arr[mid] - num) < abs(arr[right] - num):
            return arr[mid]
        else:
            return arr[right]

    def threeSumClosest(self, nums: List[int], target: int) -> int:
        nums.sort()
        nums2sum = []
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                nums2sum.append((i, j, nums[i] + nums[j]))
        nums2sum.sort(key=lambda x: x[2])

        best_err = float('inf')
        best_sum = -1
        for i in range(n):
            ni = nums[i]
            sk = self.find_closest_elem(nums2sum, target - ni)
            sum_ = ni + sk
            err = abs(target - sum_)
            if err < best_err:
                best_err = err
                best_sum = sum_

            if err == 0: break

        return best_sum

    def threeSumClosest1(self, nums: List[int], target: int) -> int:
        nums.sort()
        n = len(nums)
        best_err = float('inf')
        best_sum = -1
        best_triple = ()
        for i in range(n):
            for j in range(i + 1, n):
                ni = nums[i]
                nj = nums[j]
                target_gap = target - ni - nj
                newlist = [nums[k] for k in range(n) if k not in [i, j]]
                nk = self.find_closest_elem(newlist, target_gap, ni, nj)
                sum_ = ni + nj + nk
                err = abs(target - sum_)
                if err < best_err:
                    best_err = err
                    best_sum = sum_
                    best_triple = (ni, nj, nk)
                if err == 0: return best_sum
        print(best_triple)
        return best_sum

def main():
    sol = Solution()
    nums = [8,72,12,8,-82,16,27,85,-16,37,82,99,-75,77,92,59,10,-39,85,-66,35,-75,-42,-17,-26,-86,-68,-33,79,-71,93,35,-93,92,53,75,72,-16,41,-4,20,6,-5,63,-14,-86,97,-77,-27,-99,58,-35,55,43,-17,95,-3,-59,-5,25,-88,-59,-64,-39,-36,38,-42,56,-56,24,-12,78,-85,-90,-90,8,58,-27,-69,-79,-35,64,21,-6,51,-17,-15,78,97,89,-14,-96,-30,94,-21,69,21,-67,51,19,-36,65,97,85,43,78,-70,96,62,-64,-93,6,-63,22,-44,-16,-10,-99,-56,32,55,-89,-48,90,-4,-94,-17,43,71,61,-38,95,90,88,41,-10,95,-53,48,18,-28,82,43,-59,-21,28,-62,74,48,-63,46,17,-38,-14,46,71,-10,-52,8,33,29,-55,-16,-75,55,-85,-43,39,39,0,-52,24,90,-49,-87,94,-76,-5,-42,-21]
    target = -101

    best_sum = sol.threeSumClosest(nums, target)
    print(best_sum)
if __name__ == '__main__':
    main()
