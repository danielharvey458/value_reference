#!/bin/bash

set -eu

rm -rf build
rm -rf results

for opt_level in O1 O2 O3 Os; do
  for compiler in g++ clang++; do

    mkdir -p build/$compiler/$opt_level
    mkdir -p results/$compiler/$opt_level

    executable=./build/$compiler/$opt_level/sum
    results=./results/$compiler/$opt_level/sum.csv

    "${compiler}" --std=c++1y -I"${BENCHMARK_DIR}"/include sum.cpp -o "${executable}" -pthread -L"${BENCHMARK_DIR}"/src -lbenchmark -"${opt_level}" -fno-exceptions

    "${executable}" --benchmark_format=csv | ./cleanup.sh > "${results}";
  done
done
