from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import string, nltk, pyphen, glob, os
import numpy as np

nltk.download('punkt')
pyphen.language_fallback('en')
WordDic = pyphen.Pyphen(lang='en')

def saveNPZ(Array, OutputFile):
    np.savez_compressed(OutputFile, array1=Array)

def loadNPZ(InputFile):
    return np.load(InputFile)['array1']

def saveListTxt(Array, OutputFile):
    with open(OutputFile, 'w') as f:
        for item in Array:
            f.write('%s\n' % item)

def loadListTxt(InputFile):
    Array = []
    with open(InputFile, 'r') as f:
        Array = f.read().splitlines()

    return Array

def computeNumSyllables(word):
    Hyphs = list(WordDic.iterate(word))
    if len(Hyphs) == 0:
        return 1
    return len(Hyphs)

def computeFKScore(DataString, verbose=0):
    SentTokens = nltk.tokenize.sent_tokenize(DataString)
    nSent = len(SentTokens)
    if verbose > 0:
        print('[ INFO ]: Number of sentences is', nSent)

    WordTokens = []
    for Sent in SentTokens:
        WordTokens.extend(nltk.tokenize.word_tokenize(Sent))
    # Remove all punctuation
    Punctuation = string.punctuation + """``''"""
    # print('[ INFO ]: Punctuation dictionary - ', Punctuation)
    WordTokens = [Token for Token in WordTokens if Token not in Punctuation]
    nWords = len(WordTokens)
    if verbose > 0:
        print('[ INFO ]: Number of words is', nWords)

    nSyll = 0
    for Word in WordTokens:
        nSyll = nSyll + computeNumSyllables(Word)
    if verbose > 0:
        print('[ INFO ]: Number of syllables is', nSyll)

    FKScore = 206.835 - (1.015 * (nWords / nSent)) - (84.6 * (nSyll / nWords))
    if FKScore >= 122.22:
        print('[ WARN ]: FK Score is greater than 122.22 which is not possible. Check input and/or parsing.')
    return FKScore

def pdf2Text(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    with open(fname, 'rb') as infile:
        for page in PDFPage.get_pages(infile, pagenums):
            interpreter.process_page(page)
        infile.close()
        converter.close()
        text = output.getvalue()
        output.close
    return text

SupportedExtensions = ['*.txt', '*.text', '*.pdf', '*.dat']

def processFile(FilePath, Test='FK', verbose=0):
    if os.path.exists(FilePath) == False:
        raise Exception('[ ERR ]: File does not exist', FilePath + '. Aborting.')

    # Check if format is PDF or TXT
    _, Extension = os.path.splitext(FilePath)
    if '*' + Extension not in SupportedExtensions:
        raise Exception('[ ERR ]: Unsupported extension', Extension + '. Aborting.')

    # Get file contents as a string
    DataString = ''
    if Extension == '.pdf':
        DataString = pdf2Text(FilePath) # , pages=[])
    else: # Assuming text contents
        with open(FilePath, 'r') as File:
            DataString = File.read()

    Score = 0
    if Test == 'FK':
        if verbose > 0:
            print('[ INFO ]: Running Flesch-Kincaid Readability test on', FilePath)
        Score = computeFKScore(DataString, verbose)
        if verbose > 0:
            print('[ INFO ]: Flesch-Kincaid score for input is', Score)

    return Score

def processDir(DirPath, Test='FK', verbose=0):
    AllFiles = [glob.glob(os.path.join(DirPath, e)) for e in SupportedExtensions]
    AllSupportedFiles = [item for sublist in AllFiles for item in sublist]
    AllSupportedFiles.sort()

    AllScores = []
    Ctr = 1
    AllFiles = []
    for File in AllSupportedFiles:
        print('[ INFO ]: Processing file ' + File + ' (' + str(Ctr) + ' / ' + str(len(AllSupportedFiles)) + ')')
        Score = processFile(File, Test, verbose)
        AllScores.append(Score)
        AllFiles.append(os.path.basename(File))
        Ctr = Ctr + 1

    return AllScores, AllFiles