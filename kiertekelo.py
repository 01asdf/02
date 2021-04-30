import math
import Shapley
import FourValue
import Mintavetelezo

num_users=5
num_epochs=50
user_count_shapley=0 #Tesztelő


def numberToBinary(number):
    x = []
    a = "{0:b}".format(number)
    for j in a:
        x.append(int(j))
    for j in range(len(x), num_users):
        x.insert(0, 0)
    return x


def testusercout(user):
    count=0
    while True:
        list=numberToBinary(count)
        if list[user]==1 and sum(list)==1:
            return toInt(list)
        count+=1

def toInt(list):
    retlist=[]
    for i in list:
        retlist.append(int(i))
    reint=0
    retlist.reverse()
    for j in range(0,len(retlist)):
        reint+=retlist[j]*2**j
    return reint

adatok=[]
for i in range(0,num_epochs):
    adatok.append([])
for j in adatok:
    for i in range(0,2**num_users):
        j.append([0])

f = open("kiserlet_cnn_mnist.txt", "r")
line="1"
while line !="":
    if line =="Results\n":
        epoch=int(f.readline())
        train_group=toInt(f.readline().replace("\n","").replace("[","").replace("]","").split(", "))
        test_group=toInt(f.readline().replace("\n","").replace("[","").replace("]","").split(", "))
        accuracy=float(f.readline())
        adatok[epoch][test_group].append(accuracy)
    line=f.readline()
f.close()

forvalues_form_etalon=[]
for t in range(0,num_users):
    forvalues_form_etalon.append([])
for r in range(0,num_users+1):
    shapley_values_per_epochs=[]
    four_values_per_epochs=[]
    if r != num_users:
        user_count_shapley=testusercout(r)
        for i in adatok:
            shapley_values_per_epochs.append(Shapley.main(i[user_count_shapley],num_users))
            four_values_per_epochs.append(FourValue.main(i[user_count_shapley],num_users,r))
    if r == num_users:
        user_count_shapley=len(adatok[0])-1
        for i in adatok:
            shapley_values_per_epochs.append(Shapley.main(i[user_count_shapley],num_users))
            '''for alluser in range(0,num_users):
                forvalues_form_etalon[alluser].append(FourValue.main(i[alluser],num_users,r))'''
    #epochonkénti shapley számítás az adott user szerint


    #Átlagolás
    shapley_values=[]
    four_values=[0,0,0,0]
    for i in range(num_users):
        shapley_values.append(0)
    for i in shapley_values_per_epochs:
        for j in range(len(i)):
            shapley_values[j]+=i[j]/num_epochs
    if r != num_users:
        for i in four_values_per_epochs:
            for j in range(len(i)):
                four_values[j]+=i[j]/num_epochs
    '''else:
        for i in forvalues_form_etalon:
            for j in i:
                for g in range(len(j)):
                    four_values[g]+=j[g]/num_epochs'''
    print("----------------------------------")
    print("USER:")
    print(r)
    print("Data Shapley epochonkénti átlag")
    print(shapley_values)
    print("4 érték epochonkénti átlag")
    print(four_values)
    print((four_values[1]-four_values[0]+four_values[3]-four_values[2])/2)



