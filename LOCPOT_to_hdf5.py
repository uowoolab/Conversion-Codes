#!/usr/bin/env python3

import pymatgen.io.vasp.outputs as vasp
import argparse


def main(input, output):
    locpot = vasp.Locpot.from_file(input)
    locpot.to_hdf5(output)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str)
    parser.add_argument("output", type=str)
    args = parser.parse_args()
    input = args.input
    output = args.output
    
    main(input, output)
