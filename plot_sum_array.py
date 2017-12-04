#!/usr/bin/python

from matplotlib import pyplot

import pandas
import os
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--compiler", nargs="*")
    parser.add_argument("--opt", nargs="*")
    args = parser.parse_args()

    by_compiler = {}

    results_dir = "results"

    for compiler in args.compiler or os.listdir (results_dir):
        for opt_level in args.opt or os.listdir (os.path.join (results_dir, compiler)):
            results = os.path.join(results_dir, compiler, opt_level, "sum.csv") 
            frame = pandas.read_csv (results, index_col=1, dtype={'cpu_time':float})
            frame = frame[['name', 'cpu_time']]
            by_compiler[(compiler, opt_level)] = {name: group for name, group in frame.groupby('name')}

    sorted_keys = by_compiler.keys()
    sorted_keys.sort()

    pyplot.subplot (1, 2, 1)
    for compiler in sorted_keys:
        groups = by_compiler[compiler]
        ratio = 100 * ((groups['value']['cpu_time'] / groups['reference']['cpu_time']) - 1.0)
        ratio.plot(label=compiler)

    pyplot.grid(True)
    pyplot.title("Relative performance", fontsize=10)
    pyplot.legend(loc='best', framealpha=0.1, fontsize=10)
    pyplot.axhline(0.0, color='r')
    pyplot.xlabel('Payload (64-bit words)')
    pyplot.ylabel('Slowdown relative to pass-by-reference (%)')

    pyplot.subplot (1, 2, 2)

    for compiler in sorted_keys:
        groups = by_compiler[compiler]
        for tp, group in groups.iteritems ():
            group['cpu_time'].plot(label='{} {}'.format(tp, compiler))

    pyplot.grid(True)
    pyplot.title("Absolute perfomance", fontsize=10)
    pyplot.legend(loc='best', framealpha=0.1, fontsize=10)
    pyplot.axhline(0.0, color='r')
    pyplot.xlabel('Payload (64-bit words)')
    pyplot.ylabel('CPU Time (ns)')

    pyplot.savefig('plots/results.png')


