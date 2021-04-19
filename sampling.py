#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6


import numpy as np
from torchvision import datasets, transforms
import adatok
import random


def mnist_iid(dataset, num_users):
    """
    Sample I.I.D. client data from MNIST dataset
    :param dataset:
    :param num_users:
    :return: dict of image index
    """
    num_items = int(len(dataset)/num_users)
    dict_users, all_idxs = {}, [i for i in range(len(dataset))]
    for i in range(num_users):
        dict_users[i] = set(np.random.choice(all_idxs, num_items,
                                             replace=False))
        all_idxs = list(set(all_idxs) - dict_users[i])
    return dict_users


def mnist_noniid(dataset, num_users):
    """
    Sample non-I.I.D client data from MNIST dataset
    :param dataset:
    :param num_users:
    :return:
    """
    # 60,000 training imgs -->  200 imgs/shard X 300 shards
    num_shards, num_imgs = 200, 300
    idx_shard = [i for i in range(num_shards)]
    #ITT
    users_in_group=adatok.data.actual_train_group_in_binary
    count_users_in_group=sum(users_in_group)
    dict_users = {i: np.array([]) for i in range(adatok.data.num_users)}

    if adatok.data.image_initialization:
        idxs = np.arange(num_shards*num_imgs)
        labels = dataset.train_labels.numpy()

        # sort labels
        idxs_labels = np.vstack((idxs, labels))

        idxs_labels = idxs_labels[:, idxs_labels[1, :].argsort()]
        idxs = idxs_labels[0, :]

        #Label indexek
        label_idxs = idxs_labels[1, :]
        index_borders=[0]
        label_type=0
        for i in range(len(label_idxs)):
            if label_idxs[i]!=label_type:
                index_borders.append(i)
                label_type+=1
        index_borders.append(len(label_idxs))


        which_user_get_data=0
        for i in range(adatok.data.num_users):
            num_images_for_user_i=adatok.data.user_images_count[i]
            for j in range(len(index_borders)-1):
                if adatok.data.user_labels_percents[i][j]!=0:
                    images_from_this_label=int(adatok.data.user_labels_percents[i][j]*num_images_for_user_i/100)
                    start_index=random.randrange(index_borders[j],index_borders[j+1]-images_from_this_label)
                    adatok.data.user_images_indexes[which_user_get_data].append(start_index)
                    dict_users[which_user_get_data] = np.concatenate((dict_users[which_user_get_data], idxs[start_index:start_index+images_from_this_label]), axis=0)
            which_user_get_data+=1
        adatok.data.dict_users=dict_users

        return dict_users
    else:
        return adatok.data.dict_users



def mnist_noniid_unequal(dataset, num_users):
    """
    Sample non-I.I.D client data from MNIST dataset s.t clients
    have unequal amount of data
    :param dataset:
    :param num_users:
    :returns a dict of clients with each clients assigned certain
    number of training imgs
    """
    # 60,000 training imgs --> 50 imgs/shard X 1200 shards
    num_shards, num_imgs = 1200, 50
    idx_shard = [i for i in range(num_shards)]
    dict_users = {i: np.array([]) for i in range(num_users)}
    idxs = np.arange(num_shards*num_imgs)
    labels = dataset.train_labels.numpy()

    # sort labels
    idxs_labels = np.vstack((idxs, labels))
    idxs_labels = idxs_labels[:, idxs_labels[1, :].argsort()]
    idxs = idxs_labels[0, :]

    # Minimum and maximum shards assigned per client:
    min_shard = 1
    max_shard = 30

    # Divide the shards into random chunks for every client
    # s.t the sum of these chunks = num_shards
    random_shard_size = np.random.randint(min_shard, max_shard+1,
                                          size=num_users)
    random_shard_size = np.around(random_shard_size /
                                  sum(random_shard_size) * num_shards)
    random_shard_size = random_shard_size.astype(int)

    # Assign the shards randomly to each client
    if sum(random_shard_size) > num_shards:

        for i in range(num_users):
            # First assign each client 1 shard to ensure every client has
            # atleast one shard of data
            rand_set = set(np.random.choice(idx_shard, 1, replace=False))
            idx_shard = list(set(idx_shard) - rand_set)
            for rand in rand_set:
                dict_users[i] = np.concatenate(
                    (dict_users[i], idxs[rand*num_imgs:(rand+1)*num_imgs]),
                    axis=0)

        random_shard_size = random_shard_size-1

        # Next, randomly assign the remaining shards
        for i in range(num_users):
            if len(idx_shard) == 0:
                continue
            shard_size = random_shard_size[i]
            if shard_size > len(idx_shard):
                shard_size = len(idx_shard)
            rand_set = set(np.random.choice(idx_shard, shard_size,
                                            replace=False))
            idx_shard = list(set(idx_shard) - rand_set)
            for rand in rand_set:
                dict_users[i] = np.concatenate(
                    (dict_users[i], idxs[rand*num_imgs:(rand+1)*num_imgs]),
                    axis=0)
    else:

        for i in range(num_users):
            shard_size = random_shard_size[i]
            rand_set = set(np.random.choice(idx_shard, shard_size,
                                            replace=False))
            idx_shard = list(set(idx_shard) - rand_set)
            for rand in rand_set:
                dict_users[i] = np.concatenate(
                    (dict_users[i], idxs[rand*num_imgs:(rand+1)*num_imgs]),
                    axis=0)

        if len(idx_shard) > 0:
            # Add the leftover shards to the client with minimum images:
            shard_size = len(idx_shard)
            # Add the remaining shard to the client with lowest data
            k = min(dict_users, key=lambda x: len(dict_users.get(x)))
            rand_set = set(np.random.choice(idx_shard, shard_size,
                                            replace=False))
            idx_shard = list(set(idx_shard) - rand_set)
            for rand in rand_set:
                dict_users[k] = np.concatenate(
                    (dict_users[k], idxs[rand*num_imgs:(rand+1)*num_imgs]),
                    axis=0)

    return dict_users


def cifar_iid(dataset, num_users):
    """
    Sample I.I.D. client data from CIFAR10 dataset
    :param dataset:
    :param num_users:
    :return: dict of image index
    """
    num_items = int(len(dataset)/num_users)
    dict_users, all_idxs = {}, [i for i in range(len(dataset))]
    for i in range(num_users):
        dict_users[i] = set(np.random.choice(all_idxs, num_items,
                                             replace=False))
        all_idxs = list(set(all_idxs) - dict_users[i])
    return dict_users


def cifar_noniid(dataset, num_users):
    """
    Sample non-I.I.D client data from CIFAR10 dataset
    :param dataset:
    :param num_users:
    :return:
    """
    num_shards, num_imgs = 200, 250
    idx_shard = [i for i in range(num_shards)]
    #ITT
    users_in_group=adatok.data.actual_train_group_in_binary
    count_users_in_group=sum(users_in_group)
    dict_users = {i: np.array([]) for i in range(adatok.data.num_users)}

    if adatok.data.image_initialization:
        idxs = np.arange(num_shards*num_imgs)
        labels = np.array(dataset.targets)

        # sort labels
        idxs_labels = np.vstack((idxs, labels))

        idxs_labels = idxs_labels[:, idxs_labels[1, :].argsort()]
        idxs = idxs_labels[0, :]

        #Label indexek
        label_idxs = idxs_labels[1, :]
        index_borders=[0]
        label_type=0
        for i in range(len(label_idxs)):
            if label_idxs[i]!=label_type:
                index_borders.append(i)
                label_type+=1
        index_borders.append(len(label_idxs))


        which_user_get_data=0
        for i in range(adatok.data.num_users):
            num_images_for_user_i=adatok.data.user_images_count[i]
            for j in range(len(index_borders)-1):
                if adatok.data.user_labels_percents[i][j]!=0:
                    images_from_this_label=int(adatok.data.user_labels_percents[i][j]*num_images_for_user_i/100)
                    start_index=random.randrange(index_borders[j],index_borders[j+1]-images_from_this_label)
                    adatok.data.user_images_indexes[which_user_get_data].append(start_index)
                    dict_users[which_user_get_data] = np.concatenate((dict_users[which_user_get_data], idxs[start_index:start_index+images_from_this_label]), axis=0)
            which_user_get_data+=1
        adatok.data.dict_users=dict_users
        return dict_users
    else:
        return adatok.data.dict_users


if __name__ == '__main__':
    dataset_train = datasets.MNIST('./data/mnist/', train=True, download=True,
                                   transform=transforms.Compose([
                                       transforms.ToTensor(),
                                       transforms.Normalize((0.1307,),
                                                            (0.3081,))
                                   ]))
    num = 100
    d = mnist_noniid(dataset_train, num)
