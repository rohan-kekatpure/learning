from typing import List

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def deleteDuplicates(self, head: ListNode) -> ListNode:
        newhead = newnode = ListNode()
        node = head
        prev_val = 1000
        while node:
            if not node.next:
                if node.val != prev_val:
                    newnode.next = ListNode(node.val)
                break

            next_val = node.next.val
            if node.val != prev_val and node.val != next_val:
                newnode.next = ListNode(node.val)
                newnode = newnode.next

            prev_val = node.val
            node = node.next
        return newhead.next

