class TrieNode:
    def __init__(self, is_end=False, children=None):
        if children is None:
            self.children = {}
        else:
            self.children = children
        
        self.is_end = is_end
        
class WordDictionary:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        node = self.root
        for c in word:
            if not (c in node.children):
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True
    
    def func(self, word, curr_node):
        for i, char in enumerate(word):
            if char == '.':
                # Recursively search in all children of the current node
                for child in curr_node.children: 
                    if self.func(word[i + 1: ], curr_node.children[child]) == True:
                        return True
                return False

            # Standard Trie search
            elif not (char in curr_node.children):
                return False
            elif char in curr_node.children:
                curr_node = curr_node.children[char]            
            
        return curr_node.is_end
    
    def search(self, word: str) -> bool:
        return self.func(word, self.root)            


# Your WordDictionary object will be instantiated and called as such:
# obj = WordDictionary()
# obj.addWord(word)
# param_2 = obj.search(word)