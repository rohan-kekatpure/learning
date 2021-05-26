class Node:
    def __init__(self, val='', children=None):
        self.val = val
        if children is None:
            self.children = dict()
        else:
            self.children = children
        self.isword = False


class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word):
        node = self.root
        for c in word:
            if not (c in node.children):
                node.children[c] = Node()
            node = node.children[c]
        node.isword = True

    def searchPrefix(self, word):
        node = self.root
        for c in word:
            if len(node.children) == 0:
                return 
            if not (c in node.children):
                return
            node = node.children[c]

        return node

    def startsWith(self, prefix):
        return bool(self.searchPrefix(prefix))

    def search(self, word):
        node = self.searchPrefix(word)
        return (node is not None) and node.isword
