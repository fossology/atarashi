# Atarashi
New License Scanner Project Which Should be Integrated with FOSSology but also Work Independently.

### Requirements
- Python v3.x
- pip 

### Steps for Installation
- In install folder, make the "atarashi-install.sh" executable
- Run <./atarashi-install.sh>
- pip install -r <pathto/requirements.txt>


## Downloading license list from SPDX
- Run `python license_extractor/LicenseDownloader.py`
- The script will create a file under licenses folder and return the path on CLI.
- This file can be used with other modules.
- To update list, simply run the same command.

### Preprocessing License List
- In scripts folder, run `python LicensePreprocessor.py <path_to_licenselist.csv> <dest_to_new_list.csv>`.
- The code will return the path to preprocessed license list.
- Use this list while running modules.


### How to run
- You can check how to run any module ( CommentExtractor, CommentPreprocessor,
dameruLevenDist, getLicenses, LicensePreprocessor, pariksha, tfidf, wordFrequencySimilarity )
using `-h` or `--help` command.
- For verbose mode use `-v` or `--verbose` flag with file name
- eg. `python tfidf.py <inputFile> <licenseList> -v`

### Test
- Run pariksha (meaning *Test* in Hindi) with the name of the Agent.
- eg. `python pariksha.py tfidfcosinesim <licenseList>`

