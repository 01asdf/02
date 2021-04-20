# 02
Ahogy a programot használni kell:
1.Az adatok.py-ban és az options.py elvégzed a számodra fontos beállításokat, DE az options.py-ban a non-iid beállítást kell választani minden esetben! Ha van olyan beállítási lehetőség amit mind az options mind az adatok.py-ban megtalálsz akkor az adatok-ban állítsd be mert ezek fognak érvényrejutni a futás során!
2.Futtatod a vezerlo.py-t

Beállítások az adatok.py-ban:
Kötelező: El kell döntened, hogy az egyes résztvevők hány képpel rendelkezzenek: A user_images_count tömbben annyi pozitív egész számnak kell MINIMUM szerepelnie ahány user lesz. (Az nem baj ha több szerepel, mint ahány user van, de kevesebb ne legyen)
Választhatóak:

1.config_number: El lehet dönteni, hogy mely konfigurációs fileból szeretnéd, hogy megmond melyik résztvevőnek milyen arányban legyenek képei az egyes számokból. Ha 0 akkor a labeling.py-ban szereplő függvény kötelessége egy tömbben megadni, hogy mekkorák ezek az arányok. A tömb méretének minimum a userek számával kell egyenlőnek lennie.

2.model: megadható, hogy milyen modell legyen használva (mlp, cnn).

3.dataset: megadható, hogy milyen dataset legyen használva (mnist, cifar).

4.num_users: a résztvevők száma.

A program futási folyamata:
1. Elindul a vezerlo.py. (Jelen pillanatban dinamikusan vannak változtatva a modellek és a dataset-ek.) Ha az adatok.data.image_initialization=True akkor az adatok.py init függvénye felülírja azokat az argumentumokat amiket nála lehet beállítani, majd elindul a federated.py, de nem fog végigfutni, csak az adatok.data osztályába betöltődnek a késöbbi futásokkor használandó képek indexei.
2. Elindul a federated.py ismét, ekkor viszont már nincs kép index válogatás, hanem aaz adatok.data osztályából történik a betöltés. (Ez azért van így, mert így lehetséges 2szer egymás után ugyanazokkkal a képekkel tanítani a modellt. EZ NEM 2 KÜLÖN INDÍTÁST JELENT! A vezerlo.pyban kell megszerkesztenünk a 2 futás paramétereit és a federated.py-t futtatni)
3. A federated.py-ban a globális modellt tanítjuk be külön minden user adataival és elmentjük a lokális súlyokat (84. sortól 90.-ig)
4. Előállítunk egy tanítási kombinációt és ennek megfelelően létrehozzuk az aggregált modellt (92-től 103. sor)
5. Az aggregált modellt leteszteljük az összes lehetséges teszt koalícióra és kiírjuk az eredményeket (105.-től 109. sor)

FIGYELJ!
Ha 1 db vezérlo.py hívásban különböző képeken szeretnéd tanítani a modelleket, akkor a képek váltásakor az alábbi beállítást eszközöld: adatok.data.image_initialization=True
Ezt kötelező megtenni akkor is amikor dataset-et váltasz, hosz a 2 dataset indexei valószínűleg nem fognak megeggyezni!
