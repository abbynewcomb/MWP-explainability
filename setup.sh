#!/bin/bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";

sudo pip3 install virtualenv

virtualenv -p python3 venv

for FILE in `find code -name setup.sh -type f`; do
    echo "Running ${FILE}..."
    ( cd $(dirname ${FILE}) && sh $(basename ${FILE}) )
done
