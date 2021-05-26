# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        slow = fast = head
        
        while fast:
            slow = slow.next
            
            if fast.next:
                fast = fast.next.next
            else:
                return False
            
            if slow == fast:
                return True
                    
        return False
        
                    
