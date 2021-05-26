
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random

class Solution:
    def copyRandomList(self, head: 'Node') -> 'Node':
        """
        IDEA
        
        Two pass solution.
        
        Pass1: we copy the linked list w/o random pointers and 
               create a mapping of old nodes to new nodes.
        Pass2: we fill in random pointer information with the
               help of the map.
        """
        
        # Copy list w/o random pointers
        node = head
        sentinel = newnode = Node(-1001)
        mapping = {}
        while node:
            nextnode = Node(-1001)
            newnode.next = nextnode
            newnode = newnode.next            
            newnode.val = node.val
            mapping[id(node)] = newnode
            node = node.next
        
        # Copy random pointer information
        node = head
        newnode = sentinel.next
        while node:
            r = node.random
            if not (r is None):
                newnode.random = mapping[id(r)]
            node = node.next
            newnode = newnode.next
        
        return sentinel.next
                