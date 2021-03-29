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

def linkedlist_to_list(head: ListNode):
    node = head
    v = []
    while node:
        v.append(node.val)
        node = node.next
    return v

def list_to_linkedlist(lst):
    head = ListNode()
    node = head
    n = len(lst)
    for i in range(n - 1):
        node.val = lst[i]
        node.next = ListNode()
        node = node.next
    node.val = lst[-1]
    return head

def main():
    # x = [2, 4, 3]  # number is 4321
    # y = [5, 6, 4]
    x = [0,8,6,5,6,8,3,5,7]
    y = [6,7,8,0,8,5,8,9,7]

    n1 = list_to_linkedlist(x)
    n2 = list_to_linkedlist(y)
    s = Solution()
    n3 = s.addTwoNumbers(n1, n2)
    print(linkedlist_to_list(n3))
    from IPython import embed; embed(); exit(0)
if __name__ == '__main__':
    main()
