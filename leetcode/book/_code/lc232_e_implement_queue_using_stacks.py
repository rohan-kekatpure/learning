class Stack:
    def __init__(self):
        self.lst = []
    
    def push(self, x):
        self.lst.append(x)
    
    def pop(self):
        if len(self.lst) > 0:
            return self.lst.pop()
    
    def peek(self):
        if len(self.lst) > 0:
            return self.lst[-1]
    
    def empty(self):
        return len(self.lst) == 0
    

class MyQueue:

    def __init__(self):
        self.P = Stack()
        self.Q = Stack()

    def _QtoP(self):        
        if self.P.empty():
            while not self.Q.empty():
                self.P.push(self.Q.pop())


    def push(self, x: int) -> None:
        self.Q.push(x)        

    def pop(self) -> int:
        self._QtoP()                
        return self.P.pop()

    def peek(self) -> int:
        self._QtoP()
        return self.P.peek()

    def empty(self) -> bool:
        return self.P.empty() and self.Q.empty()        


# Your MyQueue object will be instantiated and called as such:
# obj = MyQueue()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.peek()
# param_4 = obj.empty()