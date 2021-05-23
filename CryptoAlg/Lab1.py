class AlgMath:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = ((other.y - self.y) / (other.x - self.x)) ** 2 - self.x - other.x
        y = ((other.y - self.y) / (other.x - self.x)) * (self.x - x) - self.y
        return AlgMath(x, y)

    def __sub__(self, other):
        x = ((-other.y - self.y) / (other.x - self.x)) ** 2 - self.x - other.x
        y = ((-other.y - self.y) / (other.x - self.x)) * (self.x - x) - self.y
        return AlgMath(x, y)

    def mult(self, a):
        x = ((3 * self.x ** 2 + a) / (2 * self.y)) ** 2 - 2 * self.x
        y = ((3 * self.x ** 2 + a) / (2 * self.y)) * (self.x - x) - self.y
        return AlgMath(x, y)

    def print(self):
        return f"x: {self.x} y: {self.y}"
    def res(self):
        return self.x,self.y

# e = (-1,1)
# p,q,r = AlgMath(58,139),AlgMath(56,332),AlgMath(85,35)
# print("AlgMath P: ",p.print())
# print("AlgMath Q: ", q.print())
# print("AlgMath R: ", r.print())
# print("2P = ", p.mult(e[0]).print())
# print("3Q = ", (q.mult(e[0]) + q).print())
# print("2P + 3Q = ", (p.mult(e[0]) + (q.mult(e[0]) + q)).print())
# print("2P + 3Q - R ", ((p.mult(e[0]) + (q.mult(e[0]) + q)) - r).print())
