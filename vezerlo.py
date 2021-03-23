import adatok
import federated_main
import sys

def main():
    sys.stdout=open("kimenet"+adatok.data.model+adatok.data.dataset+".txt",'w')
    adatok.init()
    federated_main.main()
    for i in adatok.data.train_groups_in_binary:
        adatok.data.actual_train_group_in_binary=i
        federated_main.main()

