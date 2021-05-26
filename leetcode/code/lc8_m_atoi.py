class Solution:
    def greater(self, s1, s2):
        l1 = len(s1)
        l2 = len(s2)
        if l1 != l2:
            return l1 > l2

        i = 0
        while (i < l1) and (s1[i] == s2[i]):
            i += 1
        if i == l1:
            return True

        return s1[i] > s2[i]

    def myAtoi(self, s: str) -> int:
        if s == '':
            return 0

        # Strip all leading whitespace
        i = 0
        while (i < len(s)) and (s[i] == ' '):
            i += 1
        s = s[i:]

        if s == '':
            return 0

        if s[0] == '-':
            sign = -1
            s = s[1:]
        elif s[0] == '+':
            sign = 1
            s = s[1:]
        else:
            sign = 1

        # Strip all leading zeros
        if s == '':
            return 0

        i = 0
        while (i < len(s)) and (s[i] == '0'):
            i += 1
        s = s[i:]

        digits = ''
        for c in s:
            if c not in list('0123456789'):
                break

            digits += c

        if digits == '':
            return 0

        MAXP = str((1 << 31) - 1)
        MAXN = str((1 << 31))
        if sign == -1:
            if self.greater(digits, MAXN):
                return -int(MAXN)

        if sign == 1:
            if self.greater(digits, MAXP):
                return int(MAXP)
        return sign * int(digits)


def main():
    sol = Solution()
    d = sol.myAtoi('2147483647')
    print(d)

if __name__ == '__main__':
    main()
