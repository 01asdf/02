import adatok
import federated_main
import sys

def main():
    for d in adatok.data.do:
        for l in adatok.data.lr:
            adatok.data.act_lr=l
            adatok.data.act_do=d
            sys.stdout=open("kimenet"+adatok.data.model+adatok.data.dataset+str(d)+"A"+str(l)+".txt",'w')
            adatok.init()
            federated_main.main()
            for i in adatok.data.train_groups_in_binary:
                adatok.data.actual_train_group_in_binary=i
                federated_main.main()

