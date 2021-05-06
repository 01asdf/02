#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6


import os
import copy
import random
import time
import pickle
import numpy as np
from tqdm import tqdm

import torch
#from tensorboardX import SummaryWriter

from options import args_parser
from update import LocalUpdate, test_inference
from models import MLP, CNNMnist, CNNFashion_Mnist, CNNCifar
from utils import get_dataset, average_weights, exp_details
import adatok

def ellentett(list1, list2):
    for i in range(0,len(list2)):
        if list1[i] == list2[i]:
            return False
    return True

def main():
    start_time = time.time()

    # define paths
    path_project = os.path.abspath('..')
    #logger = SummaryWriter('../logs')
    logger = None
    args = args_parser()
    args=adatok.arguments(args)
    exp_details(args)
    if args.gpu:
        torch.cuda.set_device(args.gpu)
    device = 'cuda' if args.gpu else 'cpu'

    # load dataset and user groups
    train_dataset, test_dataset, user_groups = get_dataset(args)
    if adatok.data.image_initialization==True:
        adatok.data.image_initialization=False
        return
    # BUILD MODEL
    if args.model == 'cnn':
        # Convolutional neural netork
        if args.dataset == 'mnist':
            global_model = CNNMnist(args=args)
        elif args.dataset == 'fmnist':
            global_model = CNNFashion_Mnist(args=args)
        elif args.dataset == 'cifar':
            global_model = CNNCifar(args=args)

    elif args.model == 'mlp':
        # Multi-layer preceptron
        img_size = train_dataset[0][0].shape
        len_in = 1
        for x in img_size:
            len_in *= x
            global_model = MLP(dim_in=len_in, dim_hidden=64,
                               dim_out=args.num_classes)
    else:
        exit('Error: unrecognized model')

    # Set the model to train and send it to device.
    global_model.to(device)
    global_model.train()
    #print(global_model)

    # copy weights
    global_weights = global_model.state_dict()

    # Training
    train_loss, train_accuracy = [], []
    val_acc_list, net_list = [], []
    cv_loss, cv_acc = [], []
    print_every = 2
    val_loss_pre, counter = 0, 0

    for epoch in tqdm(range(args.epochs)):
        local_weights, local_losses = [], []
        #print(f'\n | Global Training Round : {epoch+1} |\n')

        global_model.train()
        m = max(int(args.frac * args.num_users), 1)
        for idx in range(args.num_users):
            local_model = LocalUpdate(args=args, dataset=train_dataset,
                                      idxs=user_groups[idx], logger=logger)
            w, loss = local_model.update_weights(
                model=copy.deepcopy(global_model), global_round=epoch)
            local_weights.append(copy.deepcopy(w))
            local_losses.append(copy.deepcopy(loss))

        for sample in range(0, adatok.data.num_users*3):
            trainers=list(range(0,adatok.data.num_users))
            random.shuffle(trainers)
            trained=[]
            aggregation_weights = []
            #DataShapleynek
            for i1 in trainers:
                trained.append(i1)
                modell_to_aggregate = copy.deepcopy(global_model)
                modell_to_aggregate.to(device)
                modell_to_aggregate.train()
                aggregation_weights.append(local_weights[i1])
                avarege_w = average_weights(aggregation_weights)
                modell_to_aggregate.load_state_dict(avarege_w)
                modell_to_aggregate.eval()
                # Test inference after completion of training
                for i2 in adatok.data.test_groups_in_binary:
                    if sum(i2)==args.num_users:
                        adatok.data.actual_test_group_in_binary = i2
                        test_acc, test_loss = test_inference(args, modell_to_aggregate, test_dataset)
                        print("DataShapley\n", epoch, "\n", sample, "\n", trained, "\n",
                              adatok.data.actual_test_group_in_binary, "\n", test_acc, "\n")
        #4ertekesnek
        for i in adatok.data.train_groups_in_binary:
            if sum(i)==1:
                aggregation_weights = [local_weights[i.index(1)]]
                modell_to_aggregate = copy.deepcopy(global_model)
                modell_to_aggregate.to(device)
                modell_to_aggregate.train()
                avarege_w = average_weights(aggregation_weights)
                modell_to_aggregate.load_state_dict(avarege_w)
                modell_to_aggregate.eval()

                for i2 in adatok.data.test_groups_in_binary:
                    if i2==i:
                        adatok.data.actual_test_group_in_binary = i2
                        test_acc, test_loss = test_inference(args, modell_to_aggregate, test_dataset)
                        print("FourValues\n", epoch, "\n", i, "\n",
                              adatok.data.actual_test_group_in_binary, "\n", test_acc, "\n")

            if sum(i)==args.num_users-1:
                aggregation_weights = []
                for j in range(0,len(i)):
                    if i[j] == 1 :
                        aggregation_weights.append(local_weights[j])
                modell_to_aggregate = copy.deepcopy(global_model)
                modell_to_aggregate.to(device)
                modell_to_aggregate.train()
                avarege_w = average_weights(aggregation_weights)
                modell_to_aggregate.load_state_dict(avarege_w)
                modell_to_aggregate.eval()

                for i2 in adatok.data.test_groups_in_binary:
                    if ellentett(i2,i):
                        adatok.data.actual_test_group_in_binary = i2
                        test_acc, test_loss = test_inference(args, modell_to_aggregate, test_dataset)
                        print("FourValues\n", epoch, "\n", i, "\n",
                              adatok.data.actual_test_group_in_binary, "\n", test_acc, "\n")
            if sum(i) == args.num_users:
                aggregation_weights = []
                for k in local_weights:
                    aggregation_weights.append(k)
                modell_to_aggregate = copy.deepcopy(global_model)
                modell_to_aggregate.to(device)
                modell_to_aggregate.train()
                avarege_w = average_weights(aggregation_weights)
                modell_to_aggregate.load_state_dict(avarege_w)
                modell_to_aggregate.eval()

                for i2 in adatok.data.test_groups_in_binary:
                    if sum(i2)==1:
                        adatok.data.actual_test_group_in_binary = i2
                        test_acc, test_loss = test_inference(args, modell_to_aggregate, test_dataset)
                        print("FourValues\n", epoch, "\n", i, "\n",
                              adatok.data.actual_test_group_in_binary, "\n", test_acc, "\n")


        # update global weights
        global_weights = average_weights(local_weights)

        # update global weights
        global_model.load_state_dict(global_weights)

        loss_avg = sum(local_losses) / len(local_losses)
        train_loss.append(loss_avg)

        # Calculate avg training accuracy over all users at every epoch
        list_acc, list_loss = [], []
        global_model.eval()


if __name__ == '__main__':
    main()
