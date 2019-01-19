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

The FK readability score should be estimated as `97.6877272727273`.

## Batch Process
You can process an entire directory of text and/or PDF files and obtain summary statistics using:

`testReadability.py -d <DIRECTORY_PATH>`

The readability scores for all files are written as an numpy array `readability.npz` in `<DIRECTORY_PATH>`.

## Helper Scripts
1. To download a directory from a remote URL use:
  
    `downloadURL.py -u URL`


# Contact
Srinath Sridhar  
[ssrinath@cs.stanford.edu][1]

[1]: mailto:ssrinath@cs.stanford.edu