#!/bin/bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";

pip install virtualenv

virtualenv -p python3 venv && source venv/bin/activate

pip install -r code/requirements.txt

for FILE in `find code -name setup.sh -type f`; do
    echo "Running ${FILE}..."
    sh $(basename ${FILE})
done
