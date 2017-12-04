#!/bin/bash

set -eu

for compiler in g++ clang++; do
./build/sum_$compiler --benchmark_format=csv | ./cleanup.sh > results/$compiler.csv;
done
