# Atarashi
New License Scanner Project Which Should be Integrated with FOSSology but also Work Independently.

### Requirements
- Python v3.x
- pip 

### Steps for Installation
- In install folder, make the "atarashi-install.sh" executable
- Run <./atarashi-install.sh>
- pip install -r <pathto/requirements.txt>

### How to run
- You can check how to run any module ( CommentExtractor, CommentPreprocessor, dameruLevenDist, getLicenses, pariksha, tfidf, wordFrequencySimilarity )
using `-h` or `--help` command.
- For verbose mode use `-v` or `--verbose` flag with file name
- eg. `python tfidf.py <inputFile> <licenseList> -v`

### Test
- Run pariksha (meaning *Test* in Hindi) with the name of the Agent.
- eg. `python pariksha.py tfidfcosinesim`
