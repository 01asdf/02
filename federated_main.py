#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6


import os
import copy
import time
import pickle
import numpy as np
from tqdm import tqdm

import torch
# from tensorboardX import SummaryWriter

from options import args_parser
from update import LocalUpdate, test_inference
from models import MLP, CNNMnist, CNNFashion_Mnist, CNNCifar
from utils import get_dataset, average_weights, exp_details
import adatok


def main():
    start_time = time.time()

    # define paths
    path_project = os.path.abspath('..')
    # logger = SummaryWriter('../logs')
    logger = None
    args = args_parser()
    args = adatok.arguments(args)
    exp_details(args)
    if args.gpu:
        torch.cuda.set_device(args.gpu)
    device = 'cuda' if args.gpu else 'cpu'

    # load dataset and user groups
    train_dataset, test_dataset, user_groups = get_dataset(args)
    if adatok.data.image_initialization == True:
        adatok.data.image_initialization = False
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
    # print(global_model)

    # copy weights
    global_weights = global_model.state_dict()

    # Training
    train_loss, train_accuracy = [], []
    val_acc_list, net_list = [], []
    cv_loss, cv_acc = [], []
    val_loss_pre, counter = 0, 0

    for epoch in tqdm(range(args.epochs)):
        local_weights, local_losses = [], []

        global_model.train()
        for idx in range(args.num_users):
            local_model = LocalUpdate(args=args, dataset=train_dataset,
                                      idxs=user_groups[idx], logger=logger)
            w, loss = local_model.update_weights(model=copy.deepcopy(global_model))
            local_weights.append(copy.deepcopy(w))
            local_losses.append(copy.deepcopy(loss)) 

        '''
        for i1 in adatok.data.train_groups_in_binary:
            adatok.data.actual_train_group_in_binary = i1
            modell_to_aggregate = copy.deepcopy(global_model)

            modell_to_aggregate.to(device)
            modell_to_aggregate.train()

            aggregation_weights = []
            for j in range(len(i1)):
                if i1[j] == 1:
                    aggregation_weights.append(local_weights[j])
            avarege_w = average_weights(aggregation_weights)
            modell_to_aggregate.load_state_dict(avarege_w)

            modell_to_aggregate.eval()


            # Test inference after completion of training
            for i2 in adatok.data.test_groups_in_binary:
                adatok.data.actual_test_group_in_binary = i2
                test_acc, test_loss = test_inference(args, modell_to_aggregate, test_dataset)
                print("Results\n", epoch, "\n", adatok.data.actual_train_group_in_binary, "\n",
                      adatok.data.actual_test_group_in_binary, "\n", test_acc, "\n")
        
        '''
        # update global weights
        global_weights = average_weights(local_weights)
        global_model.load_state_dict(global_weights)

        print(test_inference(args, global_model, train_dataset)[0])

        loss_avg = sum(local_losses) / len(local_losses)
        train_loss.append(loss_avg)


if __name__ == '__main__':
    main()
