# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    """
    https://en.wikipedia.org/wiki/Cycle_detection
    Jump to section
    "Floyd's tortoise and hare"
    """    
    def detectCycle(self, head: ListNode) -> ListNode:
        slow = fast = head
        while fast:
            slow = slow.next
            
            if fast.next:
                fast = fast.next.next
            else:
                return
        
            if slow == fast:
                break
        
        if fast is None:
            return
        
        slow = head
        while slow != fast:
            slow = slow.next
            fast = fast.next        
        
        return slow