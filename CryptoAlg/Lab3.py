def gcd(a, b):
    while a != 0 and b != 0:
        print(f"a = {a},b = {b}")
        if a > b:
            print(f"a//b: {a // b}")
            a %= b
            print(f"osta: {a}")
        else:
            print(f"b//a: {b // a}")
            b %= a
            print(f"ostb: {b}")
        print("-----------")
    return a + b


def back_step(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = back_step(b, a % b)
        return d, y, x - y * (a // b)


def create_res(b):
    if b[1] < 0:
        return n + b[1]
    elif b[1] > 1:
        return 0
    else:
        return b[1]


a, n = int(input("Enter a: ")), int(input("Enter n: "))
# print(gcd(a, n))
b = back_step(a, n)
print(b)
print(create_res(b))
# if b[1] <0:print(n+b[1])
# elif b[1]>1:print(0)
# else:print(b[1])
