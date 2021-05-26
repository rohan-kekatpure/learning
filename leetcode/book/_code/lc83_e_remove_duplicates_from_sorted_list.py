from typing import List
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def deleteDuplicates(self, head: ListNode) -> ListNode:
        sentinel = prev = ListNode(0, head)
        node = head
        while node:
            if node.next and (node.val != node.next.val):
                prev.next = node
                prev = node
            else:
                prev.next = node

            node = node.next
        return sentinel.next

