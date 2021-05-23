def factorisation(n):
    arr = []
    d = 2
    while d**2 <= n:
        if n % d == 0:
            arr.append(d)
            n //= d
            print(arr)
        else:
            d += 1
    if n > 1:
        arr.append(n)
    print(arr)
    return arr

if __name__ == "__main__":
    my_number = 14031999116114101116105971071091059910497101108 #47 разрядов
    # print(len(str(my_number)))
    factorisation(my_number)
