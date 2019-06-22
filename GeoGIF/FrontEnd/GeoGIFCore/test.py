class d:
   def __init__(self,num):
     self.num = num
   def __add__(self, b):
     if b == 0:
       return self
     else:
       print(self, b)
       return b
   def __radd__(self, b):
     return self + b
   def __str__(self):
     return str(self.num)
 
a = d(1)
b = d(2)
c = d(3)
sum([a,b,c])
