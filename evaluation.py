import sys, getopt
import numpy as np

number_users=0
method=0
samples=0
epoch=0
dict_users= {i: np.array([]) for i in range(number_users)}
try:
    opts, args = getopt.getopt(sys.argv[1:],'h:n:s:d:e:')
except getopt.GetoptError:
    print('Usage: evaluation.py -n <user of numbers> -s <0: shapley, 1: sampling from random epochs, 2: samples from epoch, 3: 4 value> -d <number of samples> -e <samples from this epoch>')
    sys.exit(2)


for opt, arg in opts:
    if opt == '-h':
        print('Usage: evaluation.py -n <user of numbers> -s <0: shapley, 1: sampeling, 2: 4 value> -d <number of samples>')
        sys.exit()

    elif opt == '-n':
        number_users=int(arg)
    elif opt == '-s':
        method=int(arg)
    elif opt == '-d':
        sampels=int(arg)
    elif opt == '-e':
        epoch=int(arg)
    else:
        continue
line="line"
while line!="":
    f = open("kimenet.txt", "r")
    line=f.readline()
    if line== 'Resoults':
        print()

