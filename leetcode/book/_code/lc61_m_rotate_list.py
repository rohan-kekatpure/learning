
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def reverse(self, head):
        prev = head
        curr = head.next
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        head.next = None
        return prev

    def length(self, head):
        node = head
        i = 0
        while node:
            i += 1
            node = node.next
        return i

    def rotateRight(self, head: ListNode, k: int) -> ListNode:
        if head is None:
            return

        if head.next is None:
            return head

        length = self.length(head)
        k %= length

        tail = head
        head = self.reverse(head)

        # Rotation operation
        for _ in range(k):
            nxt = head.next
            tail.next = head
            tail = head
            tail.next = None
            head = nxt

        # reverse again
        head = self.reverse(head)
        return head


class Solution2:
    def traverse(self, head):
        if head is None:
            return 0, None

        node = head
        length = 1
        while node.next:
            length += 1
            node = node.next
        return length, node

    def rotateRight(self, head: ListNode, k: int) -> ListNode:
        if head is None: return
        if head.next is None: return head
        if k == 0: return head

        # Convert to circular linked list
        length, tail = self.traverse(head)
        tail.next = head
        k %= length
        num_forward_jumps = length - k
        for _ in range(num_forward_jumps):
            # Jump the head and tail forward
            head = head.next
            tail = tail.next

        tail.next = None
        return head


