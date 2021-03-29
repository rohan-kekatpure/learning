class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        T = [[0 for _ in range(n)] for _ in range(n)]
        T[0][0] = 1
        for i in range(1, n):
            T[i][i] = 1
            T[i - 1][i] = int(s[i - 1] == s[i])

        for w in range(2, n):
            for i in range(n - w):
                j = i + w
                if (T[i + 1][j - 1] == 1) and (s[i] == s[j]):
                    T[i][j] = 1

        # Now find the index (i, j) s.t. T[i, j] == 1 and (j - i) is largest
        mi = mj = 0
        for i in range(n):
            for j in range(i, n):
                if (T[i][j] == 1) and (j - i > mj - mi):
                    mi, mj = i, j
        return s[mi: mj + 1]

def main():
    sol = Solution()
    s = '''jaliztdispcppzgzjxnjxwbhhtbjrijyibqwrhwuscmokylygielwssuyretqnoiglvsltmhetvdoliwibrnwmdtauczcswuqxxokaykslfzgxovphdptgtrbbozdkdgawcegemkumgbyqzjrzurkdaibfwwvcxfcstvixisrcfxvnlzizlbnacxssetlsxrvcaqvzmbnzdfmtskmxmjblzgpdsjvhqhrihiajvwxbmjsncjhmilercbdbzyncrnlyrxrefaeuttkscfttqnedzvqisclbremuxmngrpgqjqkijpizkixkrgaarpknivrrirbkeddkulvlfuetbdnugzodbfufqhrpkyufhrhnnnzsenkvqsuhlbaimniusuxsnmavqbilzgsfxjykrxdkkpnneikwlucdghnikojythrpgwyzoqgraycavrivsbfuaonssmryhcykooivrxmeeowllsfeyxrznvkdpobohpzolnpbxjjxbpnlozphobopdkvnzrxyefsllwoeemxrviookychyrmssnoaufbsvirvacyargqozywgprhtyjokinhgdculwkiennpkkdxrkyjxfsgzlibqvamnsxusuinmiablhusqvknesznnnhrhfuykprhqfufbdozgundbteuflvlukddekbrirrvinkpraagrkxikzipjikqjqgprgnmxumerblcsiqvzdenqttfcskttueaferxrylnrcnyzbdbcrelimhjcnsjmbxwvjaihirhqhvjsdpgzlbjmxmkstmfdznbmzvqacvrxsltessxcanblzizlnvxfcrsixivtscfxcvwwfbiadkruzrjzqybgmukmegecwagdkdzobbrtgtpdhpvoxgzflskyakoxxquwsczcuatdmwnrbiwilodvtehmtlsvlgionqteryusswleigylykomcsuwhrwqbiyjirjbthhbwxjnxjzgzppcpsidtzilaj'''
    res = sol.longestPalindrome(s)
    print(res)

if __name__ == '__main__':
    main()
