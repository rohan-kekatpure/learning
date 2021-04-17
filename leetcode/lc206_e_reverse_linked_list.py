# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        if not head: return None

        prev = head
        curr = head.next
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        head.next = None
        return prev

def main():
    import utils as U
    lst = [1, 2, 3, 4, 5, 6, 7]
    llist = U.list_to_linkedlist(lst)
    sol = Solution()
    rev_llist = sol.reverseList(llist)
    rev_list = U.linkedlist_to_list(rev_llist)
    from IPython import embed; embed(); exit(0)

if __name__ == '__main__':
    main()
