import os, sys, argparse
import utils
import numpy as np
# import matplotlib.pyplot as plt

Parser = argparse.ArgumentParser(description='Script to print and plot summary statistics of a directory which has been processed already.')
# --------------------
# Required Arguments
# --------------------
ParseGroup = Parser.add_argument_group()
ParseGroup.add_argument('-d', '--directory', help='Path to a directory with PDF or text files.', type=str, metavar='DIRECTORY_PATH', required=True)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        Parser.print_help()
        exit()
    Args = Parser.parse_args()

    OutputNP = os.path.join(Args.directory, 'readability.npz')
    OutputTXT = os.path.join(Args.directory, 'order.txt')

    AllScores = utils.loadNPZ(OutputNP)
    print(AllScores)

    AllFiles = utils.loadListTxt(OutputTXT)
    print(AllFiles)

    AllDict = dict(zip(AllFiles, AllScores.tolist()))
    print(AllDict)