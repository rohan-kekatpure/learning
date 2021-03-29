class Solution:
    def nextval(self, table):
        n = len(table)
        val = 0
        val += 2 * table[-1]
        for j in range(1, n - 1):
            val += table[j] * table[n - j - 1]
        return val

    def numTrees(self, n: int) -> int:
        table = [0, 1]
        for i in range(2, n + 1):
            val = self.nextval(table)
            table.append(val)
        return table[-1]

def main():
    sol = Solution()
    trees = sol.numTrees(5)


if __name__ == '__main__':
    main()
