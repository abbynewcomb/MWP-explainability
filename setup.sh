#!/bin/bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";

sudo pip3 install virtualenv

virtualenv -p python3 venv && source venv/bin/activate

pip3 install -r code/requirements.txt

(cd code/graph2tree; mkdir {logs,models,out,runs,outputs})
(cd code/gts; mkdir {logs,models,out,runs,outputs})
(cd code/rnn_seq2seq; mkdir {logs,models,out,runs,outputs})
(cd code/transformer_seq2seq; mkdir {logs,models,out,runs,outputs})
