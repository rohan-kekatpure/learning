from typing import List

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        node = head
        cache = []
        while node:
            cache.append(node)
            if len(cache) > n + 1:
                cache.pop(0)
            node = node.next

        if n == len(cache):
            return head.next

        if n == 1:
            cache[0].next = None
        else:
            cache[0].next = cache[2]

        return head

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
    lst = head = [1, 2]
    n = 2
    ll = list_to_linkedlist(lst)
    sol = Solution()
    head = sol.removeNthFromEnd(ll, n)
    lst2 = linkedlist_to_list(head)
    from IPython import embed; embed(); exit(0)


if __name__ == '__main__':
    main()
