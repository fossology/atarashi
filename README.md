# Atarashi

[![Build Status](https://travis-ci.com/fossology/atarashi.svg?branch=master)](https://travis-ci.com/fossology/atarashi)

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
https://fossology.github.io/atarashi

### Requirements

- Python >= v3.5
- pip >= 18.1

## Steps for Installation

### Install

#### Install from PyPi

- `pip install atarashi`

#### Source install

- `pip install .`
- It will download all dependencies required and trigger build as well.
- Build will generate 3 new files in your current directory
    1.  `data/Ngram_keywords.json`
    2.  `licenses/<SPDX-version>.csv`
    3.  `licenses/processedList.csv`
- These files will be placed to their appropriate places by the install script.

### Installing just dependencies
- `# pip install -r requirements.txt`

### Build (optional)

- `$ python3 setup.py build`

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

### Running Docker image
1. Pull Docker image

    `docker pull fossology/atarashi:latest`
2. Run the image

    `docker run --rm -v <path/to/scan>:/project fossology/atarashi:latest <options> /project/<path/to/file>`

Since docker can not access host fs directly, we mount a volume from the
directory containing the files to scan to `/project` in the container. Simply
pass the options and path to the file relative to the mounted path.

### Test

- Run imtihaan (meaning *Exam* in Hindi) with the name of the Agent.
- eg. `python atarashi/imtihaan.py /path/to/processedList.csv <DLD|tfidf|Ngram> <testfile>`
- See `python atarashi/imtihaan.py --help` for more

## Creating Debian packages

- Install build dependencies from `debian/control`
- Install dependencies from requirements.txt
```sh
# python3 -m pip install -r requirements.txt
```
- Build the orig.tar file manually or get from github (master branch) using uscan.
```sh
$ uscan -dd
```
- Build the packages using your favourite script
```sh
$ debuild
```

## Installing Debian package
- Install the `.deb` file
- Install the missing dependencies (`Nirjas`, `textdistance`, `pyxDamerauLevenshtein`)
```sh
# python3 -m pip install textdistance>=3.0.3 pyxDamerauLevenshtein>=1.5 Nirjas>=0.0.3
```

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

## How to generate the documentation using sphinx

1. Go to project directory 'atarashi'.
2. Install Sphinx and m2r `pip install sphinx m2r` (Since this project is based on python so `pip` is already installed).
3. Initialise `docs/` directory with `sphinx-quickstart`

    ```bash
    mkdir docs
    cd docs/
    sphinx-quickstart
    ```
   - `Root path for the documentation [.]: .`
   - `Separate source and build directories (y/n) [n]: n`
   - `autodoc: automatically insert docstrings from modules (y/n) [n]: y`
   - `intersphinx: link between Sphinx documentation of different projects (y/n) [n]: y`
   - Else use the default option
4. Setup the `conf.py` and include `README.md`
   - Enable the following lines and change the insert path:

        ```python
        import os
        import sys
        sys.path.insert(0, os.path.abspath('../'))
        ```
   - Enable `m2r` to insert `.md` files in Sphinx documentation:

        ```python
        [...]
        extensions = [
          ...
          'm2r',
        ]
        [...]
        source_suffix = ['.rst', '.md']
        ```
   - Include `README.md` by editing `index.rst`

        ```rst
        .. toctree::
            [...]
            readme

        .. mdinclude:: ../README.md
        ```
5. Auto-generate the `.rst` files in `docs/source` which will be used to generate documentation

    ```bash
    cd docs/
    sphinx-apidoc -o source/ ../atarashi
    ```
6. `cd docs`
7. `make html`

This will generate file in `docs/_build/html`. Go to: index.html

You can change the theme of the documentation by changing `html_theme` in config.py file in `docs/` folder.
You can choose from {'alabaster', 'classic', 'sphinxdoc', 'scrolls', 'agogo', 'traditional', 'nature', 'haiku', 'pyramid', 'bizstyle'}
[Reference](https://www.sphinx-doc.org/en/master/usage/theming.html)
