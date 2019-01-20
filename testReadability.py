import os, sys, argparse, glob
import utils
import numpy as np

Parser = argparse.ArgumentParser(description='Script to evaluate readability of PDF or text documents.')
# --------------------
# Required Arguments
# --------------------
InputGroup = Parser.add_mutually_exclusive_group()
InputGroup.add_argument('-i', '--input', help='Path to the input PDF or text file.', type=str, metavar='INPUT_FILE')
InputGroup.add_argument('-d', '--directory', help='Path to a directory with PDF or text files.', type=str, metavar='DIRECTORY_PATH')

ParseGroup = Parser.add_argument_group()
ParseGroup.add_argument('-t', '--test', help='Enter name of readability test.', choices=['FK'], metavar='FK (Flesch-Kincaid)', type=str, required=False, default='FK')
ParseGroup.add_argument('-v', '--verbose', help='Print details.', action='store_true')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        Parser.print_help()
        exit()
    Args = Parser.parse_args()

    if Args.input:
        Score = utils.processFile(Args.input, verbose=Args.verbose)
        print('[ INFO ]: Readability score is', Score)
    elif Args.directory:
        AllScores, AllFiles = utils.processDir(Args.directory, verbose=Args.verbose)
        print('[ INFO ]: Scores -', AllScores)
        OutputNP = Args.directory + 'readability.npz'
        OutputTXT = Args.directory + 'order.txt'
        utils.saveNPZ(np.asarray(AllScores), OutputNP)
        utils.saveListTxt(AllFiles, OutputTXT)
        print('[ INFO ]: Saved to', OutputNP, 'and', OutputTXT)

        # Test = utils.loadNPZ(OutputNP)
        # print(Test)
        # print(Test == np.asarray(AllScores))

        # Files = utils.loadListTxt(OutputTXT)
        # print(Files)
