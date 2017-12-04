#!/bin/bash
set -o pipefail

sed -re 's/"(\S+)<([0-9]+)>"/\1,\2/1' \
    -e 's/name/name,payload/g'
