import math

def numberToBinary(number, users):
    x = []
    a = "{0:b}".format(number)
    for j in a:
        x.append(int(j))
    for j in range(len(x), users):
        x.insert(0, 0)
    return x

def osszegez(adatok, hanyadiknaklepbe, melyiket, num_users):
    osszeg = 0;
    for i in range(1,len(adatok)+1):
        bin = numberToBinary(i, num_users)
        if bin[melyiket] == 1 and sum(bin) == hanyadiknaklepbe:
            ellentett_dec = ellentettErteke(num_users,bin, melyiket)
            if ellentett_dec == 0:
                osszeg+=adatok[i]
            else:
                osszeg += adatok[i-1]-adatok[ellentett_dec]
    return osszeg


def hanyelem(binaris):
    x = 0
    for i in binaris:
        if i == 0:
            x += 1
    return x


def szorzo(n, k):
    x = 1
    x *= math.factorial(k - 1)
    x *= math.factorial(n - k)
    x /= math.factorial(n)
    return x


def osszehasonlito(mit, mivel, hanyadikbanelteres):
    if mit == mivel:
        return False
    for i in range(0, len(mit)):
        if i == hanyadikbanelteres:
            continue
        if mit[i] != mivel[i]:
            return False
    return True


def ellentettErteke(num_users, minek, hanyadikelem):
    for i in range(0,2**num_users):
        if osszehasonlito(numberToBinary(i,num_users), minek, hanyadikelem):
            return i


def main(number_users, adatok): #az adatok egy 1 dimenziós tömb, ahol a traingroupok bináris sorrendjében vannak az értékek
    for i in range(0, number_users):
        shapley = 0
        for hanyadiknaklepbe in range(1, number_users + 1):
            osszeg = osszegez(adatok, hanyadiknaklepbe, i, number_users)
            shapley += szorzo(number_users, hanyadiknaklepbe) * osszeg
        print("{:.3f}".format(shapley))
