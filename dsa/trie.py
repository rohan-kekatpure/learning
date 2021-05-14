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

    def _dfs(self, node, word, results):
        if node.isword:
            results.append(word)

        if len(node.children) == 0:        
            return

        for c, n in node.children.items():
            self._dfs(n, word + c, results)

    def print(self):
        results = []
        self._dfs(self.root, '', results)
        return results



def main():
    t = Trie()
    t.insert('apples')
    t.insert('app')
    t.insert('application')
    t.insert('appearence')
    t.insert('orange')

    from IPython import embed; embed(); exit(1)

if __name__ == '__main__':
    main()

