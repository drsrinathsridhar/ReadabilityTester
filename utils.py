from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import string, nltk, pyphen

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