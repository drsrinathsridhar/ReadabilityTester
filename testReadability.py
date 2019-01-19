import os, sys, argparse
import utils

Parser = argparse.ArgumentParser(description='Script to evaluate readability of PDF or text documents.')
# --------------------
# Required Arguments
# --------------------
ParseGroup = Parser.add_argument_group()
ParseGroup.add_argument('-i', '--input', help='Path to the input PDF or text file.', type=str, required=True, metavar='INPUT_FILE')
ParseGroup.add_argument('-t', '--test', help='Enter name of readability test.', choices=['FK'], metavar='FK (Flesch-Kincaid)', type=str, required=False, default='FK')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        Parser.print_help()
        exit()

    Args = Parser.parse_args()

    if os.path.exists(Args.input) == False:
        print('[ ERR ]: File does not exist', Args.input + '. Aborting.')
        exit()

    # Check if format is PDF or TXT
    _, Extension = os.path.splitext(Args.input)
    if Extension not in ['.txt', '.text', '.pdf', '.dat']:
        print('[ ERR ]: Unsupported extension', Extension + '. Aborting.')
        exit()

    # Get file contents as a string
    DataString = ''
    if Extension == '.pdf':
        DataString = utils.pdf2Text(Args.input) # , pages=[])
    else: # Assuming text contents
        with open(Args.input, 'r') as File:
            DataString = File.read()

    if Args.test == 'FK':
        print('[ INFO ]: Running Flesch-Kincaid Readability test on', Args.input)
        FKScore = utils.computeFKScore(DataString)
        print('[ INFO ]: Flesch-Kincaid score for input is', FKScore)