import utils as U

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        if l1 is None: return l2
        if l2 is None: return l1

        n1 = l1
        n2 = l2
        carry = 0
        solution_head = solution_node = ListNode()

        while n1 or n2 or (carry > 0):
            solution_node.next = ListNode()
            solution_node = solution_node.next

            v1 = v2 = 0
            if n1:
                v1 = n1.val
                n1 = n1.next

            if n2:
                v2 = n2.val
                n2 = n2.next

            tot = v1 + v2 + carry
            carry = tot // 10
            solution_node.val = tot % 10

        return solution_head.next

