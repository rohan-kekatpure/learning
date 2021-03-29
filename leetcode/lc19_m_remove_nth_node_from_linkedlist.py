# Definition for singly-linked list.

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

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

class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        i = 0
        node = head
        while i < n - 1:
            node = node.next
            i += 1

        if (node is None) or (node.next is None):
            return head
        node.next = node.next.next
        return head


def main():
    sol = Solution()
    lst = [1,2,3,4]
    lklist = list_to_linkedlist(lst)

    sol.removeNthFromEnd()
if __name__ == '__main__':
    main()

