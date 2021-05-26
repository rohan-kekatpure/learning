# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    """
    O(n) space
    O(n) time
    """
    def partition(self, head: ListNode, x: int) -> ListNode:
        left = lefthead = ListNode()
        right = righthead = ListNode()
        node = head
        while node:
            tmp = ListNode(node.val)
            if node.val < x:
                left.next = tmp
                left = left.next
            else:
                right.next = tmp
                right = right.next
            node = node.next
        left.next = righthead.next
        return lefthead.next


