#!/usr/bin/env python
"""
    getmodels: A program to extract model files from Nanopore reads.
               You must provide a read that has given a 2D read
               - i.e comes from the pass folder.
"""
import sys
import h5py
import pandas as pd
import configargparse


def get_model_location(hdf,strand):
    """ Find path for node with a model table for strand "strand". """
    for element in hdf:
        for element2 in hdf[element]:
            for element3 in hdf[element][element2]:
                try:
                    for element4 in hdf[element][element2][element3]:
                        if any("Model" in s for s in [element,element2,element3,element4]):
                            if any(strand in s for s in [element,element2,element3,element4]):
                                return element,element2,element3,element4
                except:
                    pass


def main():
    parser = configargparse.ArgParser(description='getmodels: A program to extract model files from Nanopore reads. You must provide a read that has given a 2D read - i.e comes from the pass folder.')
    parser.add('-read', '--read', type=str, dest='read', required=True, default=None, help="Provide a read file to extract the current model from.")
    args = parser.parse_args()
    hdf = h5py.File(args.read, 'r')
    try:
        template_path = "/".join(get_model_location(hdf,"template"))
        complement_path = "/".join(get_model_location(hdf,"complement"))
    except TypeError:
        print "ERROR: This file does not contain template and complement models."

        hdf.close()
        sys.exit(1)

    hdf.close()
    print "Found model date in these paths:"
    print template_path
    print complement_path
    print

    columns = ['kmer', 'level_mean', 'level_stdv']

    df = pd.read_hdf(args.read, template_path)
    df = df[columns]
    df.to_csv("template.model", sep="\t", index=False)

    df = pd.read_hdf(args.read, complement_path)
    df = df[columns]
    df.to_csv("complement.model", sep="\t", index=False)


    print "File Write Completed."
    print "Kmer length is:", len(df.kmer[0])
    print "File format is:"
    print "Kmer\tMean\tStandard Dev"


if __name__ == "__main__":
    main()
