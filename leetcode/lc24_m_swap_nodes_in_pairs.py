# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def swapPairsWithVal(self, head: ListNode) -> ListNode:
        node = head
        while node and node.next:
            node.val, node.next.val = node.next.val, node.val
            node = node.next.next
        return head

    def swapPairs(self, head: ListNode) -> ListNode:
        cur = head
        prev = None
        newhead = None
        while cur and cur.next:
            nxt = cur.next
            if not newhead:
                newhead = nxt

            tmp = nxt.next
            cur.next = tmp

            if prev:
                prev.next = nxt

            nxt.next = cur
            prev = cur
            cur = tmp

        if not newhead:
            newhead = head

        return newhead

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
    l = [1, 2]
    ll = list_to_linkedlist(l)
    sol = Solution()
    swapped = sol.swapPairs(ll)
    print(linkedlist_to_list(swapped))

if __name__ == '__main__':
    main()

