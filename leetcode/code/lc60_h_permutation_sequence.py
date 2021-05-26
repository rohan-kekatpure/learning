class Solution:
    def getPermutation(self, n: int, k: int) -> str:
        facts = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]
        k -= 1
        set_ = list(range(1, n + 1))
        answer = []
        while n > 0:
            f = facts[n - 1]
            idx, k = divmod(k, f)
            answer.append(set_[idx])
            set_.pop(idx)
            n -= 1

        return ''.join([str(c) for c in answer])

def main():
    sol = Solution()
    perm = sol.getPermutation(3, 2)
    print(perm)

if __name__ == '__main__':
    main()

