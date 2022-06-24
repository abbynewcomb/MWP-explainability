#!/bin/bash

# Training
RUN_NAME=run_${2}

if [ ${1} == 'test' ]; then
    # Testing
    python -m src.main \
        -mode test \
        -dataset ${2} \
        -run_name ${RUN_NAME} \
        -full_cv \
        ${@:3}
else
    # Training
    python -m src.main \
        -seed 12345 \
        -mode train \
        -embedding roberta \
        -emb_name roberta-base \
        -cell_type lstm \
        -hidden_size 512 \
        -depth 2 \
        -lr 1e-3 \
        -emb_lr 8e-6 \
        -batch_size 4 \
        -dropout .5 \
        -epochs ${1} \
        -dataset ${2} \
        -run_name ${RUN_NAME} \
        -full_cv \
        -save_model \
        ${@:3}
fi

