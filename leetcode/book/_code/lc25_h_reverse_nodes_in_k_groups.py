# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def reverse(self, head):
        """Reverse a linked list in O(1) space"""
        if not head:
            return None

        prev = head
        curr = head.next
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        head.next = None
        return prev

    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        dummynode = ListNode()
        prev = dummynode
        curr = head
        while curr:
            n = 0
            cprev = node = curr
            while node and n < k:
                cprev = node
                node = node.next
                n += 1

            if n < k:  # i.e. node is None
                break

            cnxt = node
            cprev.next = None
            chead = self.reverse(curr)
            prev.next = chead
            curr.next = cnxt
            prev = curr
            curr = cnxt
        return dummynode.next

