# Atarashi
New License Scanner Project Which Should be Integrated with FOSSology but also Work Independently.

# Requirements
- Python v3.x
- pip 

# Steps for Installation
- In install folder, make the "atarashi-install.sh" executable
- Run <./atarashi-install.sh>
- pip install -r <pathto/requirements.txt>

## Downloading license list from SPDX
- Run `python license_extractor/LicenseDownloader.py`
- The script will create a file under licenses folder and return the path on CLI.
- This file can be used with other modules.
- To update list, simply run the same command.
