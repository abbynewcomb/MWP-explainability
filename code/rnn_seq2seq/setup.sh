#!/bin/bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";
DIRS=(logs models out runs outputs)

for DIR in ${DIRS[@]}; do
    mkdir -p ${SCRIPT_DIR}/${DIR}
done
