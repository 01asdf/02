import numpy as np
import labeling

class data:
    outputfile=""
    config_number=0
    model='mlp'
    dataset='mnist'

    secarg=0

    # Kik legyenek a támadók
    attackers = [False, False, False, False, False]
    #attackers = [True, True, True, True, True]

    # Milyen százalékban haj0tsanak végre támadást
    miss_labeling = [0,0,0,0,0]
    #miss_labeling = [100,100,75,75,75]

    #noise = [0,0,0,0,0]
    noise = [100,100, 50, 10, 10]

    #-------------------------------------------------------------------------------------------------------------------
    #INNENTŐL MÉG SEMMI SEM HASZNÁLHATÓ
    #-------------------------------------------------------------------------------------------------------------------

    #Még nem használható
    to_lie = [0,0,0,0,0]

    data_are_correct = None
    # Hova legyenek kiírva az eredmények
    results_path = 'eredmenyek.txt'
    # A kísérlet paraméterei
    num_users = 5

    #Még nem használható
    secure_aggregation = False  # A false azt jelenti, hogy minden tanítási kombinációt minden teszt kombinációval végignéz
    # True esetén: Tanítási koalíciók: 1. Mindenki benne van, 2. Mindenki kivétel a teszelő, 3. Csak a tesztelő
    # True esetén: Tesztelési koalíciók: 1. Mindenki benne van, 2. Csak 1 résztvevő van benne

    # Melyik résztvevőnek milyen százalékban oszoljanak el az adatai a számok között [0,1,2,3,4,5,6,7,8,9]
    user_labels_percents = [
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    ]
    dict_users=None
    user_images_indexes=[]


    # Hány képet kapjon a résztvevő
    user_images_count = [
        200,200,200,200,200,
        200,200,200,200,200,
        200,200,200,200,200,
        200,200,200,200,200,
        200,200,200,200,200,
        200,200,200,200,200,
        200,200,200,200,200,
        200,200,200,200,200,
        200,200,200,200,200,
        200,200,200,200,200,
        200,200,200,200,200,
        200,200,200,200,200,
        200
    ]


    #Ezeket az init függvénynek kell kitöltenie a beállítások szerint
    train_groups_in_binary = []
    actual_train_group_in_binary = []

    test_groups_in_binary = []
    actual_test_group_in_binary = []

    #Futás közben
    actual_user=0
    image_initialization=True
    act_do=0.0
    act_lr=0.0
    users=[2,3]
    adathalmazok=['mnist','cifar']
    modellek=['mlp','cnn']
    act_users=2

def arguments(args):
    args.model=data.model
    args.dataset=data.dataset
    args.num_users=data.act_users
    args.frac=data.act_do
    args.lr=data.act_lr
    return args
def init():
    data.train_groups_in_binary = []
    data.actual_train_group_in_binary = []
    data.test_groups_in_binary = []
    data.actual_test_group_in_binary = []
    data.user_labels_percents=[]

    data.dict_users= {i: np.array([]) for i in range(data.num_users)}
    for i in range(data.num_users):
        data.user_images_indexes.append([])
    #Adatok ellenőrzése
    data.data_are_correct = is_data_correct()


    if data.config_number==0:
        data.user_labels_percents=labeling.labeling(data.num_users)
    else:
        f = open("config"+str(data.config_number)+".txt", "r")
        s= f.read()
        data.user_labels_percents.append(list(f.read().split(' ')))
        data.user_labels_percents.remove(data.user_labels_percents[len(data.user_labels_percents)-1])
    if not data.data_are_correct != False:  #Ha nem helyesek az adatok visszatérünk
        return

    if data.secure_aggregation:
        for i in range(1, 2 ** data.num_users):
            binary = numberToBinary(i)
            sum_of_binary = sum(binary)  # Hány résztvevő van a koalícióban
            if sum_of_binary == 1 or sum_of_binary == data.num_users:  # Mindenki és külön csak az 1 résztvevősök
                data.train_groups_in_binary.append(binary)
                data.test_groups_in_binary.append(binary)

            # A tanításnál azt is meg kell nézni amikor a tesztelő nincs benne
            if sum_of_binary == data.num_users - 1:
                data.train_groups_in_binary.append(binary)

    else:
        for i in range(1, 2 ** data.num_users):
            binary = numberToBinary(i)
            data.train_groups_in_binary.append(binary)
            data.test_groups_in_binary.append(binary)
        #data.train_groups_in_binary.append(numberToBinary((2**data.num_users)-1))

    data.actual_test_group_in_binary =  data.test_groups_in_binary[0]
    data.actual_train_group_in_binary = data.train_groups_in_binary[0]


# Adatok ellenőrzése (Ne tanítás közben derüljön ki, hogy valamit nem jól adtunk meg.
def is_data_correct():
    '''check_these_data = [data.attackers, data.miss_labeling, data.noise, data.user_labels_percents,
                         data.user_images_count]
    for i in check_these_data:
        if check_data(i) == False:
            return False
    for i in data.user_labels_percents:
        if len(i) < 10 and sum(i)!=100:
            print("Error: Percents are not 10 long or sum not 100: "+i)
            return False'''
    return True


def check_data(list):
    for i in list:
        if len(i) < data.num_users:
            print("Error with data: " + i)
            return False
    return True


def numberToBinary(number):
    x = []
    a = "{0:b}".format(number)
    for j in a:
        x.append(int(j))
    for j in range(len(x), data.num_users):
        x.insert(0, 0)
    return x

def get_dictusers():
    dict_users= {i: np.array([]) for i in range(sum(data.actual_train_group_in_binary))}
    k=0
    for j in range(sum(data.actual_train_group_in_binary)):
        if data.actual_train_group_in_binary[j]==1:
            dict_users[k]=data.dict_users[j]
            k+=1
    return dict_users


