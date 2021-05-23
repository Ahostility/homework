import operator

podstanovki = ([[1,15,13,0,5,7,10,4,9,2,3,14,6,11,8,12],[13,11,4,1,3,15,5,9,0,10,14,7,6,8,2,12],[4,11,10,0,7,2,1,13,3,6,8,5,9,12,15,14],
    [6,12,7,1,5,15,13,8,4,10,9,14,0,3,11,2],[7,13,10,1,0,8,9,15,14,4,6,12,11,2,5,3],[5,8,1,13,10,3,4,2,14,15,12,7,6,0,9,11],
    [14,11,4,12,6,13,15,10,2,3,8,1,0,7,5,9],[4,10,9,2,13,8,0,14,6,11,1,12,7,15,5,3]])

def binar(string):
    bytelist = []
    for i in string:
        if i != ' ': bytelist.append(bin(ord(i) - 848)[2:])
        else: bytelist.append('00100000')
    finalstring = ''.join(bytelist)
    return finalstring
    
def forward_encryption(l,r,x,block):
    block += 32
    step2 = (int(r, base=2) + int(x, base=2)) % 2**32
    step3 = bin(step2)[2:]
    while len(step3) < 32:
        step3 = '0' + step3

    list1 = []
    list2 = []
    for i in range(8):
        list1.append(step3[:4])
        step3 = step3[4:]
        list2.append(bin(podstanovki[i][(int(list1[i],base=2))])[2:])
        while len(list2[i]) != 4:
            list2[i] = '0' + list2[i]  
    step4 = ''.join(list2)
    step4 = step4[11:] + step4[:11]
    
    trans = []
    for i in range(len(l)):
        trans.append(str(operator.xor(int(step4[i]),int(l[i]))))
    l = r
    r = ''.join(trans)
    if block == 256: block = 0  
    x = binar(key)[block:block+32]
    return l,r,x,block

def reverse_encryption(l,r,x,block):
    block += 32
    step2 = (int(r, base=2) + int(x, base=2)) % 2**32
    step3 = bin(step2)[2:]
    while len(step3) < 32:
        step3 = '0' + step3

    list1 = []
    list2 = []
    for i in range(8):
        list1.append(step3[:4])
        step3 = step3[4:]
        list2.append(bin(podstanovki[i][(int(list1[i],base=2))])[2:])
        while len(list2[i]) != 4:
            list2[i] = '0' + list2[i]
    step4 = ''.join(list2)
    step4 = step4[11:] + step4[:11]

    trans = []
    for i in range(len(l)):
        trans.append(str(operator.xor(int(step4[i]),int(l[i]))))
    l = r
    r = ''.join(trans)
    if block == 256: 
        block = 0 
        x = binar(key)[(256-(block+32)):]
    else: x = binar(key)[(256-(block+32)):(256-block)]
    return l,r,x,block
    
text = 'ФУНИКОВ '
key = 'АЛИНА ПОШЛА В ЛЕС СОБИРАТЬ ГРИБЫ'
block = 0
L = binar(text)[:block+32]
R = binar(text)[block+32:]
X = binar(key)[:block+32]
print('Исходные данные: ', L, R)

#Shifr
for j in range(24):
    L,R,X,block = forward_encryption(L,R,X,block)
    #print(L,R,X,block)
X = binar(key)[(256-(block+32)):]
for k in range(8):
    L,R,X,block = reverse_encryption(L,R,X,block)
    #print(L,R,X,block)
print('Выходной блок шифрования = ', L, R)

#Deshifr
'''block = 0
for a in range(8):
    L,R,X,block = reverse_encryption(L,R,X,block)
X = binar(key)[:block+32]
for b in range(24):
    L,R,X,block = forward_encryption(L,R,X,block)
print('Выходной блок дешифрования = ', L, R)'''





