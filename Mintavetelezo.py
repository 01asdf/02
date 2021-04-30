from random import randrange


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

def numberToBinary(number, num_users):
    x = []
    a = "{0:b}".format(number)
    for j in a:
        x.append(int(j))
    for j in range(len(x), num_users):
        x.insert(0, 0)
    return x

def main(eredmenyek, number_users, number_of_samples):
    adatok=[]
    for i in range(len(eredmenyek)):
        adatok.append([numberToBinary(i, number_users),eredmenyek[i]])

    minta_eredmenyek=[]
    for i in range(0,number_users):
        minta_eredmenyek.append(0)

    for i in range(0,number_users):
        for j in range(0,number_of_samples):
            index=randrange(len(eredmenyek))
            minta_eredmenyek[i]+=adatok[index][1]-ellentettErteke(adatok,adatok[index],i)[1]
    for i in range(len(minta_eredmenyek)):
        minta_eredmenyek[i]=minta_eredmenyek[i]/number_of_samples
    return minta_eredmenyek
