

class Number:
    def __init__(self,n) -> None:
        self.n=n
    def __iadd__(self,value):
        self.n+=value.n
        print(value)
        return self
    def __add__(self,value):
        self.n+=value.n
        print(value)
        return self
    def add(self,value):
        self.n+=value.n
        print(value)
        return self
    def __repr__(self) -> str:
        return str(self.n)
n1=Number(50)
n2=Number(2)
n2+n1
n2.__add__(n1)
print(n2)




