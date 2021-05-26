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

def main():
    import utils as U
    lists = [[1, 4, 5], [1, 3, 4], []]
    linked_lists = []
    for lst in lists:
        linked_lists.append(U.list_to_linkedlist(lst))

    sol = Solution()
    merged = sol.mergeKLists(linked_lists)
    merged_list = U.linkedlist_to_list(merged)

if __name__ == '__main__':
    main()
