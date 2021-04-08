from typing import List
from heapq import heapify, heappop, heappush

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        # Initialize heap
        minheap = []
        for listnum, head in enumerate(lists):
            if head:
                item = (head.val, listnum, head)
                minheap.append(item)
        heapify(minheap)

        newhead = sortednode = ListNode()

        # Main loop
        while minheap:
            sortednode.next = ListNode()
            sortednode = sortednode.next

            # Pop min val from heap
            val, listnum, node = heappop(minheap)
            sortednode.val = val
            if node.next:
                heappush(minheap, (node.next.val, listnum, node.next))

        return newhead.next

def linkedlist_to_list(head: ListNode):
    node = head
    v = []
    while node:
        v.append(node.val)
        node = node.next
    return v

def list_to_linkedlist(lst):
    n = len(lst)
    if n == 0: return None
    head = ListNode()
    node = head

    for i in range(n - 1):
        node.val = lst[i]
        node.next = ListNode()
        node = node.next
    node.val = lst[-1]
    return head

def main():
    lists = [[1, 4, 5], [1, 3, 4], []]
    linked_lists = []
    for lst in lists:
        linked_lists.append(list_to_linkedlist(lst))

    sol = Solution()
    merged = sol.mergeKLists(linked_lists)
    merged_list = linkedlist_to_list(merged)
    from IPython import embed; embed(); exit(0)

if __name__ == '__main__':
    main()
