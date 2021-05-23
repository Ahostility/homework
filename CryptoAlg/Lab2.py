from Lab1 import AlgMath


def dec_in_2(num):
    pow = []
    i = 1
    n=0
    numn = []
    while i <= num:
        # print(f"I = {i}")
        if i & num:
            pow.append(i)
            numn.append(n)
        # print(f"first{i}")
        i <<= 1
        n+=1
        # print(f"second{i}")
    # print(numn)
    return pow, numn


def delitel(lis):
    lis_del = []
    for i in lis:
        if i == 1:
            lis_del.append(1)
        elif i == 2:
            lis_del.append(2)
        else:
            lis_del.append(i//2)
    return lis_del


def res_sum(xy:tuple,del_lsit:list):
    print(del_lsit)
    pass


if __name__ == '__main__':
    e = (-1, 1)
    n = 121
    p = AlgMath(58,139)
    print(p.print())
    print(p.res())
    list_dec = dec_in_2(n)
    print('stepeni',list_dec[1])
    print('number_elem',list_dec[0])
    points = [p]
    pp = AlgMath(p.res()[0],p.res()[1])
    # print(list_dec[0])
    lst = list_dec[1]
    lst.reverse()
    # print(lst)
    arr = str(n) + '*P = '
    for i in range(len(lst)):
        arr += '2^(' + str(i) + ')*P + '

    print(arr[:-3])
    for i in range(len(list_dec[0])):
        q = AlgMath(points[-1].x,points[-1].y)
        if list_dec[0][i]%2 == 0:
            # print(list_dec[1][i])
            for j in range(len(list_dec[1])-i):
                q = q.mult(-1)
                # print(f" enter P * {j} {q.res()}")
            # print(f" enter P {q.res()}")
            points.append(q)
    newP = []
    string =''
    res = AlgMath(0,0)
    for alg in points[1:]:
        newP.append((alg.x,alg.y))
        string +='('+ str(alg.x)+','+str(alg.y)+') + '
        res+= alg
    # print(newP,res.res())
    for i in points:
        res += alg
    print(string[:-3], '=', '(' + str(res.x) + ',' + str(res.y) + ')')
