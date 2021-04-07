import adatok
import federated_main
import sys

def main():

    for db in range(0,2):
        for d in adatok.data.do:
            for l in adatok.data.lr:
                for a in adatok.data.adathalmazok:
                    for u in adatok.data.users:
                        for m in adatok.data.modellek:
                            adatok.data.model=m
                            adatok.data.act_users=u
                            adatok.data.num_users=u
                            adatok.data.dataset=a
                            adatok.data.act_lr=l
                            adatok.data.act_do=d

                            adatok.init()
                            if adatok.data.image_initialization==True:
                                federated_main.main()
                            federated_main.main()
                            #sys.stdout=open("teszt_"+str(u)+"_"+str(db)+"_"+m+"_"+a+"_"+str(d)+"_"+str(l)+".txt",'w')
                            '''
                            for i in adatok.data.train_groups_in_binary:
                                adatok.data.actual_train_group_in_binary=i
                                federated_main.main()'''

main()
