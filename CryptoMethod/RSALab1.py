from math import gcd
from random import randint


def find_primes(n: int) -> list:
    lst = [2]
    for i in range(3, n + 1, 2):
        if (i > 10) and (i % 10 == 5):
            continue
        for j in lst:
            if j * j - 1 > i:
                lst.append(i)
                break
            if (i % j == 0):
                break
        else:
            lst.append(i)

    return lst


def generate_PQ(f: int, list_number: list) -> int:
    res = list_number[list_number.index(f):]
    # print(res)
    index = randint(0, len(res))
    return res[index]


def prime(a: int) -> bool:
    b = 2
    while b * b <= a and a % b != 0:
        b += 1
    return b * b > a


def find_rasp(first, second):
    if prime(first) is True and prime(second) is True:
        n = first * second  # MOD
        m = (first - 1) * (second - 1)  # Fun Eiylera
        return n, m
    else:
        print("Try again")


def find_double_empty(tuplnm: tuple, i=2) -> tuple:
    exp = 0
    d = 0
    n = tuplnm[0]
    m = tuplnm[1]
    while i < m:
        if gcd(i, m) == 1:  # open_exp взаимопростое число
            d = i
            print(f"exp = {d}")
            break
        else:
            i += 1
    i = 2
    while i < n:
        if (d * i) % m == 1:  # secret_exp
            exp = i
            print(f"d = {exp}")
            break
        else:
            i += 1
    return exp, d


def create_origin_list(origin: str) -> list:
    list_sym = []
    for char in origin:
        symbol = ord(char) - 96
        list_sym.append(symbol)
    return list_sym


def cod_origin_list(origin: list) -> str:
    symbol = ""
    for index in origin:
        symbol += chr(index + 96)
    return symbol


def encript_RSA(origin: str, abc: list, expd: tuple, nm_tuple: tuple) -> list:
    # tuple(exp,n) - open key
    exp = expd[0]
    n = nm_tuple[0]
    i = 1
    shifr = []
    while i != len(origin) + 1:
        shifr.append(int(abc[i - 1]) ** exp % n)
        print(f"C: {i} = {shifr[i - 1]}")
        i += 1
    print(f"Cipher = {shifr}")
    return shifr


def decryp_RSA(shifrotext: list, d: int, n: int) -> list:
    # tulpe(d,n) - secret key
    i = 1
    origin_text = []
    while i != len(shifrotext) + 1:
        origin_text.append(int(shifrotext[i - 1]) ** d % n)
        print('origin', i, ' = ', origin_text[i - 1])
        i += 1
    print(f"origin_text =  {origin_text}")
    return origin_text


if __name__ == "__main__":
    prim = max(find_primes(1000))
    print(generate_PQ(prim, find_primes(10000)))
    p = int(generate_PQ(prim, find_primes(10000)))
    # p = int(input("input p: "))
    q = int(generate_PQ(prim, find_primes(10000)))
    # q = int(input("input q: "))
    print(f"p = {p}, q = {q}")
    origin_message = input("input origin message: ")
    ABC = create_origin_list(origin_message)
    print(f"ABC: {ABC}")
    nm = find_rasp(p, q)
    print(f"nm: {nm}")
    expd = find_double_empty(nm)
    print(f"expd: {expd}")
    shifr_list = encript_RSA(origin_message, ABC, expd, nm)
    print(shifr_list)
    arr_text = decryp_RSA(shifr_list, expd[1], nm[0])
    print(arr_text)
    print(f"our text: {cod_origin_list(arr_text)}")