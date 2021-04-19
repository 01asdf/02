import adatok
import numpy as np
import torch
import random

'''
Bemenetek:
    labels: 1 dimenziós tenzor ami a labeleket tartalmazza
    images: 4 dimenziós tenzor:
        1. dimenzió: a tenzorban szereplő képek száma
        2. dimenzió: ??? Nem sikerült megfejtenem. Értéke mindíg 1, számomra teljesen feleslegesnek tűnik, max optimalizációra tudok gondolni
        3. és 4. dimenzió: A 20x20 pixeles képeket 28x28-as leképzésben olvassuk be. A 3. és 4. dimenziók ezen 28x28 "pixelt" tartalmazzák
'''


def attack(images, labels):
    lastrandom = 0
    # Megnézzük, hogy az adott résztvevő támadó e. Ha nem visszatérünk a manipulálatlan bemenettel
    if not adatok.data.attackers[adatok.data.actual_user]:
        return images, labels

    # Megnézzük, hogy a támadó megvalósít e misslabeling támadást
    if adatok.data.miss_labeling[adatok.data.actual_user] != 0:
        # Ha igen, akkor a labeleken végigmegyünk
        for i in range(torch.numel(labels)):
            # A támadás valószínűségében lecseréljük a labeleket
            if random.randint(0, 100) < adatok.data.miss_labeling[adatok.data.actual_user]:
                labels[i] = random_label(labels[i])

    # Megnézzük, hogy a támadó megvalósít e noise támadást
    if adatok.data.noise[adatok.data.actual_user] != 0:
        # Ha igen, akkor végigmegyünk a képek minden egyes pixelén
        for i in range(len(images)):
            for j in range(len(images[i])):
                for k in range(len(images[i][j])):
                    for r in range(len(images[i][j][k])):
                        # A támadás valószínűségében lecseréljük a pixeleket
                        if random.randint(0, 100) < adatok.data.noise[adatok.data.actual_user]:
                            lastrandom = randompixel(lastrandom)
                            images[i][j][k][r] = lastrandom
    return images, labels


# függvény ami az előző random számtól eltérőt ad vissza a [-1, 1] tartományból
def randompixel(lastrandom):
    while True:
        a = random.random() * 2 - 1
        if a != lastrandom:
            return a


# Függvény ami az inputnak kapott label helyett egy piztosan másikat ad vissza a [0, 9] tartományból
def random_label(label):
    while True:
        a = random.randint(0, 9)
        if a != label:
            return a
