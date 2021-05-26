class Solution:
    def isPalindrome_(self, head: ListNode) -> bool:
        node = head
        lst = []
        while node:
            lst.append(node.val)
            node = node.next
        
        return lst == lst[::-1]

    def isPalindrome(self, head: ListNode) -> bool:
        node = head
        l = 0
        while node:
            l += 1
            node = node.next
        
        mid = l // 2
        
        # Travel to mid position
        right_head = head
        for i in range(mid):
            right_head = right_head.next                    
        
        # Reverse the list from right_head
        prev = None
        curr = right_head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        
        lnode = head
        rnode = prev
        for i in range(mid):
            if lnode.val != rnode.val:
                return False
            lnode = lnode.next
            rnode = rnode.next
            
        return True
            
           