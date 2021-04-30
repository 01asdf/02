import adatok
import federated_main
import sys

def main():
    for db in range(0,5):
        for a in adatok.data.adathalmazok:
            adatok.data.image_initialization=True
            for m in adatok.data.modellek:
                adatok.data.model=m
                adatok.data.dataset=a
                #sys.stdout=open("kiserlet_"+m+"_"+a+"_"+str(adatok.data.config_number)+"_"+str(db)+".txt",'w')
                if adatok.data.image_initialization:
                    adatok.init()
                    federated_main.main()

                federated_main.main()


main()
