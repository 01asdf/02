from numpy import double
import math



def osszegez(adatok,hanyadiknaklepbe, melyiket):
    osszeg=0;
    for i in adatok:
        if i[0][melyiket]==1 and sum(i[0])==hanyadiknaklepbe:
            ellentett=ellentettErteke(adatok,i,melyiket)
            if ellentett == None:
                ellentett=[[1,1],[0],0]


            hozzaadni=i[1]-ellentett[1]

            osszeg+=hozzaadni
    return osszeg



def hanyelem(binaris):
    x=0
    for i in binaris:
        if i==0:
            x+=1
    return x

def szorzo(n,k):
    x=1
    x*=math.factorial(k-1)
    x*=math.factorial(n-k)
    x/=math.factorial(n)
    return x

def osszehasonlito(mit, mivel, hanyadikbanelteres):
    if mit[hanyadikbanelteres]==mivel[hanyadikbanelteres]:
        return False
    for i in range(0,len(mit)):
        if i==hanyadikbanelteres:
            continue
        if mit[i]!=mivel[i]:
            return False
    return True

def ellentettErteke(adatok, minek,hanyadikelem):
    for i in adatok:
        if osszehasonlito(i[0],minek[0],hanyadikelem):
            return i

def main(eredmenyek, number_users):
    shapleyk=[]
    for i in range(number_users):
        shapleyk.append(0)
    adatok=[]
    for i in range(len(eredmenyek)):
        adatok.append([numberToBinary(i, number_users),eredmenyek[i]])
    for user in range(0,number_users):
        shapley=0
        for hanyadiknaklepbe in range(1,number_users+1):
            osszeg=osszegez(adatok, hanyadiknaklepbe, user)

            shapley+=szorzo(number_users,hanyadiknaklepbe)*osszeg
        shapleyk[user]=shapley
    shapleyk.reverse()
    return shapleyk


def numberToBinary(number, num_users):
    x = []
    a = "{0:b}".format(number)
    for j in a:
        x.append(int(j))
    for j in range(len(x), num_users):
        x.insert(0, 0)
    return x
