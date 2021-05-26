class Solution:
    def romanToInt(self, s: str) -> int:
        if s == '': return 0

        SYMBOLS_MAP = {
            'I': 1,
            'IV': 4,
            'V': 5,
            'IX': 9,
            'X': 10,
            'XL': 40,
            'L': 50,
            'XC': 90,
            'C': 100,
            'CD': 400,
            'D': 500,
            'CM': 900,
            'M': 1000
        }

        SYMBOLS_LIST = ['I', 'V', 'X', 'L', 'C', 'D', 'M']
        symbols = []
        n = len(s)
        i = 0
        while i <= n - 2:
            current = s[i]
            nxt = s[i + 1]
            if SYMBOLS_LIST.index(nxt) > SYMBOLS_LIST.index(current):
                # Special symbol
                symbols.append(current + nxt)
                i += 2
            else:
                symbols.append(current)
                i += 1

        if i == n - 1:
            symbols.append(s[i])

        return sum(SYMBOLS_MAP[k] for k in symbols)


