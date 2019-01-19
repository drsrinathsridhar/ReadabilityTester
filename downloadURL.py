import wget, argparse, os, sys
from bs4 import BeautifulSoup
import requests
import utils

Parser = argparse.ArgumentParser(description='Script to evaluate readability of PDF or text documents.')
ParseGroup = Parser.add_argument_group()
ParseGroup.add_argument('-u', '--url', help='Enter the URL.', type=str, required=True)
ParseGroup.add_argument('-o', '--out-dir', help='Enter the output directory. Will be created if does not exist.', type=str, required=True)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        Parser.print_help()
        exit()
    Args = Parser.parse_args()

    print('[ INFO ]: Downloading all supported files', utils.SupportedExtensions, 'from', Args.url)

    if os.path.exists(Args.out_dir) == False:
        os.makedirs(Args.out_dir)

    Req = requests.get(Args.url)
    Data = Req.text
    Soup = BeautifulSoup(Data, features="lxml")

    for link in Soup.find_all('a'):
        File = link.get('href')
        _, Extension = os.path.splitext(File)
        if '*' + Extension in utils.SupportedExtensions:
            print(File)
            wget.download(Args.url + '/' + File, Args.out_dir)
            print('\n', end='')
