def numberToBinary(number, num_users):
    x = []
    a = "{0:b}".format(number)
    for j in a:
        x.append(int(j))
    for j in range(len(x), num_users):
        x.insert(0, 0)
    return x

def main(eredmenyek, number_users, whitch_user_four_values):
    adatok=[]
    for i in range(len(eredmenyek)):
        adatok.append([numberToBinary(i, number_users),eredmenyek[i]])

    eredmenyek=[]
    for i in range(0,4):
        eredmenyek.append(0)

    for i in adatok:
        if sum(i[0]) == 0:
            eredmenyek[0]=i[1]
        if sum(i[0]) == number_users:
            eredmenyek[3]=i[1]
        if sum(i[0]) == 1 and i[0][whitch_user_four_values]==1:
            eredmenyek[1]=i[1]
        if sum(i[0]) == number_users-1 and i[0][whitch_user_four_values]==0:
            eredmenyek[2]=i[1]

    return eredmenyek
