from typing import List
from collections import OrderedDict

class Solution:
    def grayCode(self, n):
        # Idea:
        # Key observation is that XORing a bit string p with _any_ power
        # of 2 will give another bitstring q such that p and q differ by
        # exactly one bit.
        #
        # We then XOR the previous element of our result list with powers
        # of 2 between 0 and n - 1, and generate n bit patterns. Some of
        # these bit patterns will have been used previously and some not.
        # There has to be at least one bit pattern out of these n which
        # has not been used. This is because among all the possible
        # graycode sortings of numbers between 0 to (2**n - 1), at least
        # one sorting must have one of the n bit strings as a neighbor of
        # the previous element. Thus a greedy approach will work, and we should
        # not need backtracking.
        #
        # We use an OrderedDict to keep track of previously generated values

        res = OrderedDict()
        res.update({0: None})
        prev = 0
        count = 1
        maxcount = 2 ** n
        while count < maxcount:
            for i in range(n):
                c = prev ^ (1 << i)
                if c not in res:
                    res.update({c: None})
                    prev = c
                    count += 1
                    break
        return res

