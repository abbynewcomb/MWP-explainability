#!/bin/bash

RUN_NAME=run_${2}

if [ ${1} == 'train' ]; then
    # Training                                                                                      
    python -m src.main \
        -seed 12345 \
        -mode train \
        -embedding roberta \
        -emb_name roberta-base \
        -emb1_size 768 \
        -hidden_size 256 \
        -depth 2 \
        -lr 2e-4 \
        -emb_lr 8e-6 \
        -batch_size 4 \
        -dropout .1 \
        -epochs ${1} \
        -early_stopping ${1} \
        -dataset ${2} \
        -run_name ${RUN_NAME} \
        -full_cv \
        -save_model \
        ${@:3}

else
    # Testing or input reduction
    python -m src.main \
        -mode ${1} \
        -dataset ${2} \
        -run_name ${RUN_NAME} \
        ${@:3}
fi

