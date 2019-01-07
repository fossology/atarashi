# Atarashi

Open source software is licensed using open source licenses. There are many
of open source licenses around and adding to that, open source software
packages involve sometimes multiple licenses for different files.

Atarashi provides different methods for scanning for license statements in
open source software. Unlike existing rule-based approaches - such as the
Nomos license scanner from the FOSSology project - atarashi implements multiple
text statistics and information retrieval algorithms.

Anticipated advantages is an improved precision while offering an as easy
as possible approach to add new license texts or new license references.

Atarashi is designed to work stand-alone and with FOSSology. More info at
http://fossology.github.io/atarashi

### Requirements

- Python v3.x
- pip

## Steps for Installation

### Installing dependencies

Dependencies are required before building Atarashi. You can install them in
following ways:

- `pip install -r requirements.txt`

OR

- `# python setup.py install_deps`

However, the dependencies are installed while installing Atarashi (running
[install command](#install))

### Build (optional)

- `$ python setup.py build`
- Build will generate 3 new files in your current directory
    1.  `data/Ngram_keywords.json`
    2.  `licenses/<SPDX-version>.csv`
    3.  `licenses/processedList.csv`
- These files will be placed to their appropriate places by the install script.

### Install

- `# python setup.py install`

## How to run

Get the help by running `atarashi -h` or `atarashi --help`

### Example

- Running **DLD** agent

    `atarashi -a DLD /path/to/file.c`
- Running **wordFrequencySimilarity** agent

    `atarashi -a wordFrequencySimilarity /path/to/file.c`
- Running **tfidf** agent
    - With **Cosine similarity**

        `atarashi -a tfidf /path/to/file.c`

        `atarashi -a tfidf -s CosineSim /path/to/file.c`
    - With **Score similarity**

        `atarashi -a tfidf -s ScoreSim /path/to/file.c`
- Running **Ngram** agent
    - With **Cosine similarity**

        `atarashi -a Ngram /path/to/file.c`

        `atarashi -a Ngram -s CosineSim /path/to/file.c`
    - With **Dice similarity**

        `atarashi -a Ngram -s DiceSim /path/to/file.c`
    - With **Bigram Cosine similarity**

        `atarashi -a Ngram -s BigramCosineSim /path/to/file.c`
- Running in **verbose** mode

    `atarashi -a DLD -v /path/to/file.c`
- Running with custom CSVs and JSONs
    - Please reffer to the build instructions to get the CSV and JSON
    understandable by atarashi.
    - `atarashi -a DLD -l /path/to/processedList.csv /path/to/file.c`
    - `atarashi -a Ngram -l /path/to/processedList.csv -j /path/to/ngram.json /path/to/file.c`


### Test

- Run imtihaan (meaning *Exam* in Hindi) with the name of the Agent.
- eg. `python atarashi/imtihaan.py /path/to/processedList.csv <DLD|tfidf|Ngram> <testfile>`
- See `python atarashi/imtihaan.py --help` for more

## Creating Debian packages

- Install dependencies
```
# apt-get install python3-setuptools python3-all debhelper
# pip install stdeb
```
- Create Debian packages
```
$ python3 setup.py --command-packages=stdeb.command bdist_deb
```
- Locate the files under `deb_dist`

## License

SPDX-License-Identifier: GPL-2.0

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2
as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
