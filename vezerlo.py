import adatok
import federated_main
import sys

def main():
    for a in adatok.data.adathalmazok:
        adatok.data.image_initialization=True
        for m in adatok.data.modellek:
            adatok.data.model=m
            adatok.data.dataset=a

            if adatok.data.image_initialization:
                adatok.init()
                federated_main.main()

            federated_main.main()
            return
                            

main()
