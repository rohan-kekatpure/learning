# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def swapPairsWithVal(self, head: ListNode) -> ListNode:
        node = head
        while node and node.next:
            node.val, node.next.val = node.next.val, node.val
            node = node.next.next
        return head

    def swapPairs(self, head: ListNode) -> ListNode:
        cur = head
        prev = None
        newhead = None
        while cur and cur.next:
            nxt = cur.next
            if not newhead:
                newhead = nxt

            tmp = nxt.next
            cur.next = tmp

            if prev:
                prev.next = nxt

            nxt.next = cur
            prev = cur
            cur = tmp

        if not newhead:
            newhead = head

        return newhead

