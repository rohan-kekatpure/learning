# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def reverseBetween(self, head: ListNode, left: int, right: int) -> ListNode:
        sentinel = ListNode(0, head)  # save for returning
        prev = sentinel
        node = head
        pos = 1
        prev_left = next_right = leftnode = rightnode = None
        while pos <= right:
            if pos == left:
                prev_left = prev
                leftnode = node
            if pos == right:
                next_right = node.next
                rightnode = node

            prev = node
            node = node.next
            pos += 1

        # Reversal loop
        prev = next_right
        curr = leftnode
        count = 0
        while count <= right - left:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
            count += 1
        prev_left.next = rightnode
        return sentinel.next

