import sys, getopt
import numpy as np
import Shapley

number_users = 0
method = 0
samples = 0
epoch = 0
dict_users = {i: np.array([]) for i in range(number_users)}
try:
    opts, args = getopt.getopt(sys.argv[1:], 'h:n:s:d:e:')
except getopt.GetoptError:
    print(
        'Usage: evaluation.py -n <user of numbers> -s <0: shapley, 1: sampling from random epochs, 2: samples from epoch, 3: 4 value> -d <number of samples> -e <samples from this epoch>')
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print(
            'Usage: evaluation.py -n <user of numbers> -s <0: shapley, 1: sampeling, 2: 4 value> -d <number of samples>')
        sys.exit()

    elif opt == '-n':
        number_users = int(arg)
    elif opt == '-s':
        method = int(arg)
    elif opt == '-d':
        sampels = int(arg)
    elif opt == '-e':
        epoch = int(arg)
    else:
        continue
line = "line"
f = open("kimenet.txt", "r")

epokok=3
users=2

adatok=[]

for i in range(epokok):
    adatok.append([])
for i in range(len(adatok)):
    for j in range(2**users-1):
        adatok[i].append([])
def dec_from_binary(binary):
    dec=0
    len_binary=len(binary)
    for i in range(len_binary):
        dec+=int(binary[i])*2**(len_binary-1-i)
    return dec
while line != "":
    line = f.readline()
    if line == 'Resoults\n':
        e=int(f.readline())
        train = f.readline().replace('[','').replace(']','').replace('\n','').split(", ")
        test = f.readline().replace('[','').replace(']','').replace('\n','').split(", ")
        val = float(f.readline())

        adatok[e][dec_from_binary(train)-1].append(val)

print("Shapley:")
shapleynek=[]
for i in adatok[0]:
    shapleynek.append(i[0])
Shapley.main(users,shapleynek)
print()
print("LOO")





def LOO(adatok, melyiket, num_users):
    bin=[]
    for i in range(num_users):
        bin.append(1)
    bin[melyiket]=0
    dec = dec_from_binary(bin)
    return adatok[0]-adatok[dec]


def numberToBinary(number, users):
    x = []
    a = "{0:b}".format(number)
    for j in a:
        x.append(int(j))
    for j in range(len(x), users):
        x.insert(0, 0)
    return x


print(str(LOO(shapleynek,0,2)))
