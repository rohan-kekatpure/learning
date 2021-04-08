from typing import List

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        n = len(s)
        w = len(words)
        k = len(words[0])
        whash = hash(''.join(sorted(words)))
        indices = []
        for i in range(n - k * w + 1):
            substr = s[i: i + k * w]
            substr_words = [substr[j: j + k] for j in range(0, k * w, k)]
            substr_words_hash = hash(''.join(sorted(substr_words)))
            if whash == substr_words_hash:
                indices.append(i)

        return indices

def main():
    s = "wordgoodgoodgoodbestword"
    words = ["word", "good", "best", "good"]

    sol = Solution()
    indices = sol.findSubstring(s, words)
    print(indices)

if __name__ == '__main__':
    main()


