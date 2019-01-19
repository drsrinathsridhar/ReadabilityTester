import os, sys, argparse, string, nltk, pyphen
nltk.download('punkt')
pyphen.language_fallback('en')
WordDic = pyphen.Pyphen(lang='en')

def computeNumSyllables(word):
    Hyphs = list(WordDic.iterate(word))
    if len(Hyphs) == 0:
        return 1
    return len(Hyphs)

def computeFKScore(DataString):
    SentTokens = nltk.tokenize.sent_tokenize(DataString)
    nSent = len(SentTokens)
    print('[ INFO ]: Number of sentences is', nSent)

    WordTokens = []
    for Sent in SentTokens:
        WordTokens.extend(nltk.tokenize.word_tokenize(Sent))
    # Remove all punctuation
    Punctuation = string.punctuation + """``''"""
    # print('[ INFO ]: Punctuation dictionary - ', Punctuation)
    WordTokens = [Token for Token in WordTokens if Token not in Punctuation]
    nWords = len(WordTokens)
    print('[ INFO ]: Number of words is', nWords)

    nSyll = 0
    for Word in WordTokens:
        nSyll = nSyll + computeNumSyllables(Word)
    print('[ INFO ]: Number of syllables is', nSyll)

    FKScore = 206.835 - (1.015 * (nWords / nSent)) - (84.6 * (nSyll / nWords))
    if FKScore >= 122.22:
        print('[ WARN ]: FK Score is greater than 122.22 which is not possible. Check input and/or parsing.')
    return FKScore


Parser = argparse.ArgumentParser(description='Script to evaluate readability of PDF or text documents.')
# --------------------
# Required Arguments
# --------------------
ParseGroup = Parser.add_argument_group()
ParseGroup.add_argument('-i', '--input', help='Path to the input PDF or text file.', type=str, required=True)
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
        print('[ TODO ]: PDF not implemented yet.')
        exit()
    else: # Assuming text contents
        with open(Args.input, 'r') as File:
            DataString = File.read()

    if Args.test == 'FK':
        print('[ INFO ]: Running Flesch-Kincaid Readability test on', Args.input)
        FKScore = computeFKScore(DataString)
        print('[ INFO ]: Flesch-Kincaid score for input is', FKScore)