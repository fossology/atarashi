# Atarashi

[![Build Status](https://github.com/fossology/atarashi/actions/workflows/build-test.yml/badge.svg)](https://github.com/fossology/atarashi/actions/workflows/build-test.yml)

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

- Python >= v3.10
- pip >= 25.0
- poetry >= 2.0.0

## Steps for Installation

### Install

#### Install from PyPi

- `pip install atarashi`

#### Source install

- ```shell
  poetry install
  poetry run preprocess
  ```
- It will download all dependencies required and trigger build as well.
- Build will generate 3 new files in your current directory
    1.  `data/Ngram_keywords.json`
    2.  `licenses/<SPDX-version>.csv`
    3.  `licenses/processedList.csv`
- These files will be placed to their appropriate places by the install script.

### Build (optional)

- `poetry build`

## How to run

Get the help by running `atarashi -h` or `atarashi --help`

### Example

- Running the **Cascade** agent (recommended)

    `atarashi -a Cascade /path/to/file.c`

  See [The Cascade agent](#the-cascade-agent) for what it does and what it returns.
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

## The Cascade agent

`Cascade` is the precision-first agent. It tries the cheapest reliable evidence
first and abstains rather than guess:

1. **`SPDX-License-Identifier`** — an author-declared tag, resolved to a license
   expression. Highest precision available, and no matching required.
2. **Exact text** — the input normalizes to a known license verbatim.
3. **Token-sequence match** — a license notice or body embedded in the input,
   scored by the longest contiguous matched run and by how much of the reference
   is covered.
4. **`UNKNOWN`** — no confident match.

Stages 2 and 3 run on the extracted comment block rather than the raw file, so
code is not matched as if it were license prose. Stage 1 runs on the raw text,
because a tag is a literal string that comment extraction may reformat.

**Abstention is the normal outcome, not an error.** On real source files carrying
an SPDX tag, about 72% have no license prose at all once the tag is stripped —
there is nothing to identify, and `UNKNOWN` is the correct answer.

### What it returns

A matched license carries the span, because a compliance reviewer needs to see the
text, not just a label:

```json
{
  "shortname": "Apache-2.0",
  "sim_type": "SequenceCoverage",
  "sim_score": 1.0,
  "matched_start": 21,
  "matched_end": 149,
  "matched_text": "Licensed under the Apache License, Version 2.0 (the \"License\") ...",
  "description": "matched chars 21:149 (run 22 tokens)"
}
```

Offsets index the text that was scanned — the extracted comment block, or the file
itself when extraction is unavailable.

A resolved tag carries the whole expression, so `AND`, `OR` and `WITH` survive.
A flat list of shortnames cannot distinguish `MIT AND Apache-2.0` from
`MIT OR Apache-2.0`, and would drop the exception from
`GPL-2.0 WITH Classpath-exception-2.0` — which changes what the license permits:

```json
{
  "shortname": "GPL-2.0",
  "sim_type": "SPDXIdentifier",
  "sim_score": 1.0,
  "expression": "GPL-2.0 WITH Classpath-exception-2.0"
}
```

### The reference index

Real files carry short license *notices* and one-line references, not license
bodies — "Licensed under the Apache License, Version 2.0, see LICENSE for details."
appears in no license text anywhere. Alongside the license list, the agent indexes
a notice layer built from scancode-toolkit's rules:
`atarashi/data/licenses/notice_rules.json`, 28k units across 2,024 keys.

1,038 of those keys are whole expressions — `Apache-2.0 WITH LLVM-exception` — because
the compound rules carry the register untagged files use. A file saying "under the
Apache License v2.0 with LLVM Exceptions" is matched as one unit and reported as both
licenses, each result carrying the `expression` it came from.

That artifact is committed, so **installing Atarashi never pulls scancode-toolkit
in**. Regenerate it only when you want to track a newer ScanCode:

```
pip install scancode-toolkit          # build-time only
python scripts/build_references.py
```

On macOS scancode needs libmagic — `brew install libmagic`, then set
`TYPECODE_LIBMAGIC_PATH=/opt/homebrew/lib/libmagic.dylib` and
`TYPECODE_LIBMAGIC_DB_PATH=/opt/homebrew/share/misc/magic.mgc`.

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
