#!/bin/bash

# Training
RUN_NAME=run_${2}

if [ ${1} == 'test' ]; then
    # Testing
    python -m src.main \
        -mode test \
        -dataset ${2} \
        -run_name ${RUN_NAME} \
        -full_cv
else
    # Training
    python -m src.main \
        -seed 12345 \
        -mode train \
        -embedding roberta \
        -emb_name roberta-base \
        -emb_lr 8e-6 \
        -heads 8 \
        -d_model 512 \
        -d_ff 2048 \
        -encoder_layers 6 \
        -decoder_layers 6 \
        -lr 1e-8 \
        -batch_size 4 \
        -epochs ${1} \
        -early_stopping ${1} \
        -dataset ${2} \
        -run_name ${RUN_NAME} \
        -full_cv \
        -save_model
fi

