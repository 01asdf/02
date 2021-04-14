import adatok
import federated_main
import sys

def main():
    adatok.data.image_initialization=True
    #sys.stdout=open("teszt_"+str(u)+"_"+str(db)+"_"+m+"_"+a+"_"+str(d)+"_"+str(l)+".txt",'w')
    #sys.stdout=open("kimenet.txt", "w")
    adatok.init()
    if adatok.data.image_initialization==True:
        federated_main.main()

    federated_main.main()
    return


main()
