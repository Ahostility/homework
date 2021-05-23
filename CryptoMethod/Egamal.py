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
            if i % j == 0:
                break
        else:
            lst.append(i)
    # print(lst)
    return lst


def generate_random_prime(f: int, list_number: list) -> int:
    res = list_number[list_number.index(f):]
    # print(res)
    index = randint(0, len(res))
    # print(res[index])
    return res[index]


def prime(a: int) -> bool:
    b = 2
    while b * b <= a and a % b != 0:
        b += 1
    # print(b*b>a)
    return b * b > a


def gcd(a: int, b: int) -> int:
    # print("\n------NOD------\n")
    while b != 0:
        a, b = b, a % b
    return a


def generate_prime_factors(n: int) -> list:#спсок примитивных элементов
    i = 2
    prime_factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            if i not in prime_factors:
                prime_factors.append(i)
    if n > 1:
        prime_factors.append(n)
    print(prime_factors)
    return prime_factors


def find_primitive_root(p:int) -> int:#выбор примитивных элементов
    order = p - 1
    if p == 2:
        return 1
    prime_factors = generate_prime_factors(order)
    while True:
        g = randint(2, order)
        flag = False
        for factor in prime_factors:
            if pow(g, order // factor, p) == 1:
                flag = True
                break
        if flag:
            continue
        print(f"g {g}")
        return g


def create_rand_XK(p:int) -> int:
    randXK = randint(2, p - 2)
    while gcd(randXK, p - 1) != 1:  # целое число x or k (1 < x or k < p-1)
        randXK = randint(2, p - 2)
    # print(print(f"randXK {randXK}"))
    return randXK


def enter_data() -> tuple:
    primeP = generate_random_prime(max(find_primes(1000)),
                                   find_primes(10000))  # сгенерировано случайное простое число p -"
    primeG = find_primitive_root(primeP)  # Выбрано число g, являющееся первообразным корнем p
    randX = create_rand_XK(primeP)
    randY = pow(primeG, randX, primeP)  # y = g^x(modp)
    return primeP, primeG, randX, randY


def encript_EG(msg:str, p:int, g:int, y:int) -> list:
    res = []
    string = ""
    for i in range(len(msg)):
        randK = create_rand_XK(
            p)  # Выбран сессионный ключ - случайное целое число k (1 < k < p-1), взаимно простое с p-1
        a = pow(g, randK, p)
        res.append((a, ((y ** randK) * ord(msg[i])) % p))
        print(f"Вычислено значение a[{i}] = g^k mod p: ", res[i][0])
        print(f"Вычислено значение b[{i}] = (y^k)M mod p: ", res[i][1])
    for i in range(0, len(res)):
        string += f"({res[i][0]}, {res[i][1]}),"
    print("Шифротекст: ", string[:-1])
    return res


def decrypt_EG(cipher_text: list, p: int, x: int) -> str:
    M = []
    our_text = ""
    """
    a = shifrotext[i][0]
    b = shifrotext[i][1]
    
    """
    for i in range(len(cipher_text)):
        M.append((cipher_text[i][1] * (cipher_text[i][0] ** (p - 1 - x))) % p)
        our_text += chr(M[i])
    return our_text


if __name__ == "__main__":
    key = enter_data()
    print(key)
    print(f"public key: (p,g,y) = {key[0], key[1], key[3]}")
    print(f"secret key x: {key[2]}")
    origin_text = input("origin text: ")
    shifrotext = encript_EG(origin_text, key[0], key[1], key[3])
    # print(shifrotext)
    origin = decrypt_EG(shifrotext, key[0], key[2])
    print(f"Origin text: {origin}")
