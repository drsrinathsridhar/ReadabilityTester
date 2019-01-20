import os, sys, argparse, csv
import utils
import numpy as np
# import matplotlib.pyplot as plt

Parser = argparse.ArgumentParser(description='Script to analyze accepted papers of CVPR.')
# --------------------
# Required Arguments
# --------------------
ParseGroup = Parser.add_argument_group()
ParseGroup.add_argument('-d', '--directory', help='Path to a directory with these files: cvpr_20XX.csv, mainconfarxiv_db.csv, order.txt, papers.csv, readability.npz.', type=str, metavar='DIRECTORY_PATH', required=True)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        Parser.print_help()
        exit()
    Args = Parser.parse_args()

    ReadScores = utils.loadNPZ(os.path.join(Args.directory, 'readability.npz'))
    FileNames = utils.loadListTxt(os.path.join(Args.directory, 'order.txt'))

    # papers.csv contains the file names from order.txt,cvpr_2018.csv contains the paper IDs in the same order
    with open(os.path.join(Args.directory, 'papers.csv'), 'r', encoding='utf-8') as PapNames, open(os.path.join(Args.directory, 'papers.csv'), 'r', encoding='utf-8') as PapIDs:
        PapNameReader = csv.reader(PapNames)
        PapIDReader = csv.reader(PapIDs)
        for row in PapNameReader:
            print(row)
            exit()
