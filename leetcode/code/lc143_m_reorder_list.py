# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reorderList(self, head: ListNode) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        if not head: return
        if not head.next: return
        
        # Create list of nodes
        nodes = []
        node = head
        while node:
            nodes.append(node)
            node = node.next
        
        # Relink
        n = len(nodes)
        i = 0
        j = n - 1
        while i < n // 2:
            revnode = nodes[j]
            nodes[i].next = nodes[j]
            nodes[j].next = nodes[i + 1]
            i += 1
            j -= 1
            
        nodes[i].next = None
        
        
                