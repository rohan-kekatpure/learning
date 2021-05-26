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
