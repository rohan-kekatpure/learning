from typing import List

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def deleteDuplicates(self, head: ListNode) -> ListNode:
        newhead = newnode = ListNode()
        node = head
        prev_val = 1000
        while node:
            if not node.next:
                if node.val != prev_val:
                    newnode.next = ListNode(node.val)
                break

            next_val = node.next.val
            if node.val != prev_val and node.val != next_val:
                newnode.next = ListNode(node.val)
                newnode = newnode.next

            prev_val = node.val
            node = node.next
        return newhead.next

def main():
    import utils as U
    sol = Solution()
    nums = [1, 1, 1, 1, 2, 3, 4, 4, 4, 5, 6, 6]
    head = U.list_to_linkedlist(nums)
    newhead = sol.deleteDuplicates(head)
    lst = U.linkedlist_to_list(newhead)
    print(lst)

if __name__ == '__main__':
    main()
