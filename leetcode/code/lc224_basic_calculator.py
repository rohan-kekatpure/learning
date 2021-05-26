class Solution:
    def parse(self, s):
        tokens = []
        n = len(s)
        i = 0
        while i < n:
            if s[i] == ' ': 
                i += 1
            elif s[i] in '()+-':                
                tokens.append(s[i])
                i += 1                
            elif s[i] in '0123456789':
                numtoken = ''
                while i < n and s[i] in '0123456789':
                    numtoken += s[i]
                    i += 1

                tokens.append(numtoken)

        return tokens

    def func(self, tokens, i, res):
        pass

    def calculate(self, s: str) -> int:
        tokens = self.parse(s)


def main():
    sol = Solution()
    tokens = sol.parse('-(-3)')

    print(tokens)


if __name__ == '__main__':
    main()