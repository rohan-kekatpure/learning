class Solution:
    """
    O(n) time, O(1) space
    Not my solution
    """
    def insertionSortList(self, head: ListNode) -> ListNode:
    dummy_head = ListNode()    
    curr = head
    
    while curr:
        prev_pointer = dummy_head
        next_pointer = prev_pointer.next
        
        while next_pointer:            
            if curr.val < next_pointer.val:
                break 
                            
            prev_pointer = prev_pointer.next
            next_pointer = next_pointer.next
         
        temp = curr.next        
        curr.next = next_pointer
        prev_pointer.next = curr
        curr = temp
        
    return dummy_head.next


class Solution:
    """
    O(n) time, O(n) space
    """
    def insertionSortList(self, head: ListNode) -> ListNode:
        if not head: return
        if not head.next: return head
        
        vals = []
        node = head
        
        # Copy nodes into array
        while node:
            vals.append(node.val)
            node = node.next
        
        # Insertion sort
        n = len(vals)
        for i in range(1, n):
            j = i - 1
            key = vals[i]
            while j >= 0 and key < vals[j]:
                vals[j + 1] = vals[j]
                j -= 1
            vals[j + 1] = key
        
        # Build new list
        sentinel = node = ListNode()
        for v in vals:
            nxt = ListNode(v)
            node.next = nxt
            node = node.next
        return sentinel.next
        