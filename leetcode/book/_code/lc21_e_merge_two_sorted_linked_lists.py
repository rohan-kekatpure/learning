# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        head = node = ListNode()

        p = l1
        q = l2

        while p and q:
            node.next = ListNode()
            node = node.next

            if p.val < q.val:
                node.val = p.val
                p = p.next
            else:
                node.val = q.val
                q = q.next

        if p: node.next = p
        if q: node.next = q

        return head.next
