# ReadabilityTester
Scripts to estimate the readability of text or PDF files. Currently only supports the Flesch-Kincaid readability test.

## Requirements
- nltk
- pyphen
- pdfminer.six
- Optional: matplotlib
- Optional: numpy

## Usage
Run the following command for a sample. Use the `-h` flag for usage instructions.

`testReadability.py -i data/wikipedia.txt`

## Batch Process
You can process an entire directory of text and/or PDF files and obtain summary statistics by:

`testReadability.py -d <DIRECTORY_PATH>`