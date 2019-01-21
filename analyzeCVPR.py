import os, sys, argparse, csv
import utils
import numpy as np
import matplotlib.pyplot as plt

Parser = argparse.ArgumentParser(description='Script to analyze accepted papers of CVPR.')
# --------------------
# Required Arguments
# --------------------
ParseGroup = Parser.add_argument_group()
ParseGroup.add_argument('-d', '--directory', help='Path to a directory with these files: cvpr_20XX.csv, mainconfarxiv_db.csv, order.txt, papers.csv, readability.npz.', type=str, metavar='DIRECTORY_PATH', required=True)

class CVPRPaper():
    def __init__(self, ID=-1, Title='', Authors=[], PaperFName='', SupFName='', AcceptedAs='Poster', ReadScore=-1):
        self.ID = ID # Paper ID
        self.Title = Title # Paper title
        self.Authors = Authors # List of authors
        self.PaperFName = PaperFName # File name of the paper
        self.SupFName = SupFName # File name of the supplementary file
        self.AcceptedAs = AcceptedAs # Options: Oral, Spotlight, Poster
        self.ReadScore = ReadScore # The readability score, usually Fleisch-Kincaid

    def __str__(self):
        Str = str(self.ID) + ', ' + self.Title + ', ' + str(self.Authors) + ', ' + self.PaperFName + ', ' + self.SupFName + ', ' + self.AcceptedAs + ', ' + str(self.ReadScore)
        return Str

def getHardestPaper(AllParsedPapers):
    LowestScore = 1000
    HardestPaper = None
    for Paper in AllParsedPapers:
        if Paper.ReadScore < LowestScore:
            HardestPaper = Paper
            LowestScore = Paper.ReadScore

    return HardestPaper

def getEasiestPaper(AllParsedPapers):
    HighestScore = 0
    EasiestPaper = None
    for Paper in AllParsedPapers:
        if Paper.ReadScore > HighestScore:
            EasiestPaper = Paper
            HighestScore = Paper.ReadScore

    return EasiestPaper

if __name__ == '__main__':
    if len(sys.argv) == 1:
        Parser.print_help()
        exit()
    Args = Parser.parse_args()

    ReadScores = utils.loadNPZ(os.path.join(Args.directory, 'readability.npz'))
    FileNames = utils.loadListTxt(os.path.join(Args.directory, 'order.txt'))
    BestPapers = utils.loadListTxt(os.path.join(Args.directory, 'best_papers.txt'))
    FileNames = [F.lower() for F in FileNames]
    BestPapers = [F.lower() for F in BestPapers]
    FileScoreDict = dict(zip(FileNames, ReadScores))

    ValidReadScores = []
    BestPaperScores = []
    NumAuthors = []
    PaperIDs = []
    TitleLengthWords = []
    TitleLengthCharacters = []

    # papers.csv contains the file names from order.txt, cvpr_2018.csv contains the paper IDs in the same order
    AllParsedPapers = []
    with open(os.path.join(Args.directory, 'papers.csv'), 'r', encoding='ascii') as PapNames, open(os.path.join(Args.directory, 'cvpr_2018.csv'), 'r', encoding='utf-8') as PapIDs:
        PapNameReader = csv.reader(PapNames)
        PapIDReader = csv.reader(PapIDs)
        for IDDetails, TitleDetails in zip(PapIDReader, PapNameReader):
            # Extract title file name
            TitleIdx = [i for i, s in enumerate(TitleDetails) if 'content_cvpr_2018/papers/' in s]
            IDIdx = [i for i, s in enumerate(IDDetails) if 'content_cvpr_2018/CameraReady/' in s]
            ID = int(os.path.basename(IDDetails[IDIdx[0]]).replace('.pdf', ''))
            Title = os.path.basename(TitleDetails[TitleIdx[0]])
            Authors = TitleDetails[1:TitleIdx[0]]
            Authors = [A.replace('\\', '').strip() for A in Authors]
            SupFName = os.path.basename(TitleDetails[TitleIdx[0]+1])
            ReadScore = FileScoreDict[Title.lower()]
            if ReadScore < 60 or ReadScore > 123:
                print('[ WARN ]: Readability score is messed up for PaperID', ID)
                # print(ID, Title, Authors, Title, SupFName, 'Poster', ReadScore)
            else:
                ValidReadScores.append(ReadScore)
                NumAuthors.append(len(Authors))
                PaperIDs.append(ID)
                TitleLengthCharacters.append(len(TitleDetails[0]))
                TitleLengthWords.append(len(TitleDetails[0].split(' ')))
                Paper = CVPRPaper(ID, Title, Authors, Title, SupFName, 'Poster', ReadScore)
                AllParsedPapers.append(Paper)
                # if len(Authors) > 20:
                #     print(Paper)
            if Title.lower() in BestPapers:
                BestPaperScores.append(ReadScore)

    # Start compiling stats
    ValidReadScores = np.asarray(ValidReadScores)
    NumAuthors = np.asarray(NumAuthors)
    PaperIDs = np.asarray(PaperIDs)
    BestPaperScores = np.asarray(BestPaperScores)
    TitleLengthCharacters = np.asarray(TitleLengthCharacters)
    TitleLengthWords = np.asarray(TitleLengthWords)
    print('[ INFO ]: Average readability score of all accepted papers:', np.mean(ValidReadScores))
    print('[ INFO ]: Average readability score of 6 best papers:', np.mean(BestPaperScores))

    print('[ INFO ]: Hardest paper to read\n', getHardestPaper(AllParsedPapers))
    print('[ INFO ]: Easiest paper to read\n', getEasiestPaper(AllParsedPapers))

    plt.figure(0)
    plt.hist(ValidReadScores, bins=50)
    plt.figure(1)
    plt.scatter(ValidReadScores, NumAuthors)
    plt.figure(2)
    plt.scatter(ValidReadScores, PaperIDs)
    plt.figure(3)
    plt.scatter(ValidReadScores, TitleLengthWords)
    plt.figure(4)
    plt.scatter(ValidReadScores, TitleLengthCharacters)
    plt.show()