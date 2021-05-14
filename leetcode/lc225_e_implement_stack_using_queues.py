class Queue:
    def __init__(self):
        self.queue = []
    
    def push(self, num):
        self.queue.append(num)
    
    def pop(self):
        return self.queue.pop(0)

    def top(self):
        return self.queue[0]

    def empty(self):
        return len(self.queue) == 0    
    

class MyStack:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.P = Queue()
        self.Q = Queue()

    def push(self, x: int) -> None:
        """
        Push element x onto stack.
        O(n)
        """
        self.P.push(x)
        while not self.Q.empty():
            self.P.push(self.Q.pop())
        self.P, self.Q = self.Q, self.P

    def pop(self) -> int:
        """
        Removes the element on top of the stack and returns that element.
        """
        return self.Q.pop()

    def top(self) -> int:
        """
        Get the top element.
        """
        return self.Q.top()

    def empty(self) -> bool:
        """
        Returns whether the stack is empty.
        """
        return self.Q.empty()


# Your MyStack object will be instantiated and called as such:
# obj = MyStack()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.top()
# param_4 = obj.empty()