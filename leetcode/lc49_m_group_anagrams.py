from typing import List

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        anagram_dict = {}
        for s in strs:
            key = ''.join(sorted(s))
            if key in anagram_dict:
                anagram_dict[key].append(s)
            else:
                anagram_dict[key] = [s]
        return list(anagram_dict.values())

def main():
    sol = Solution()
    strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    groups = sol.groupAnagrams(strs)
    print(groups)

if __name__ == '__main__':
    main()
