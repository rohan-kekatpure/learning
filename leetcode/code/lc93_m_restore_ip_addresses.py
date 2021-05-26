from typing import List

class Solution:
    def __init__(self):
        self.ipaddresses = []

    def isvalid(self, chunk):
        if len(chunk) == 1 and (0 <= int(chunk) <= 9):
            return True

        return ('1' <= chunk[0] <= '9') and (int(chunk) < 256)

    def func(self, block, s, ipaddr):
        if block < 4 and s == '':
            return

        if block == 3:
            if self.isvalid(s):
                ipaddr += [s]
                self.ipaddresses.append(ipaddr)
            return

        # Recursive block
        for i in range(1, 4):
            if self.isvalid(s[:i]):
                self.func(block + 1, s[i:], ipaddr + [s[:i]])

    def restoreIpAddresses(self, s: str) -> List[str]:
        self.func(0, s, [])
        return list(set(['.'.join(i) for i in self.ipaddresses]))

def main():
    sol = Solution()
    s = '010010'
    addrs = sol.restoreIpAddresses(s)
    print(addrs)

if __name__ == '__main__':
    main()
