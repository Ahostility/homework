'''TeoryIntMethod

"This code was created by Mikhail Tretyak
and the right to dispose of it remains with him(c)"

Task №1
Create NOD ALG and to get answer of question len and age
'''

class NOD:
    def __init__(self,a,b):
        self._a = a
        self._b = b

    def start(self):
        return self.wide_nod(self._a,self._b)

    def wide_nod(self,a,b):
        if not b:
            return (1, 0, a)
        y, x, g = self.wide_nod(b, a % b)
        return x, y - (a // b) * x, g

def gcd(a, b):
    while a != 0 and b != 0:
        print(f"a = {a},b = {b}")
        if a > b:
            print(f"a//b: {a//b}")
            a %= b
            print(f"osta: {a}")
        else:
            print(f"b//a: {b//a}")
            b %= a
            print(f"ostb: {b}")
        print("-----------")
    return a+b

    # print(a)
# list = (12,1)
list = (147000000,14031999)
# list = (17,6)
# 149597870700
# nod = NOD(12,4)
# nod = NOD(list[0],list[1])
# print(nod.start())
# print(bezout_recursive(list[0],list[1]))
print(f"Enter gcd: {gcd(list[0],list[1])}")
# print(14031999*3)