import adatok
import federated_main
import sys


def main():
    for db in range(0, 2):
        for a in adatok.data.adathalmazok:
            for u in adatok.data.users:
                for m in adatok.data.modellek:
                    adatok.data.model = m
                    adatok.data.act_users = u
                    adatok.data.num_users = u
                    adatok.data.dataset = a
                    adatok.data.image_initialization = True

                    # sys.stdout=open("teszt_"+str(u)+"_"+str(db)+"_"+m+"_"+a+"_"+str(d)+"_"+str(l)+".txt",'w')
                    sys.stdout = open("kimenet.txt", "w")
                    adatok.init()
                    if adatok.data.image_initialization == True:
                        federated_main.main()

                    federated_main.main()
                    return


main()
