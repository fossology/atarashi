
September 8 2017

Test File Version: 1.0
--------------------------


1.0 Description

These are the license test files that correpsond to the SPDX License List. The test files are gernerated using the SPDX 
License List JSON data files as denoted below. The test files are meant to be used by license scanning tools for test purposes
around license detection.

Each test file has 3 sections: 

 - Header at the top which has the test file version and License List used along with disclaimers, etc.,.
 - Licensein the middle where either the "standard header" or "license text" for the specific license is placed.
   If the license, according to the License List, uses a stanndard header then that is placed here. Else, the licnese
   text is used.
 - Code which has some fake, and likey wont compile, C like code just in case tools need something.

The name of each test file is of the form "spdx short identifier for the license".c. 

For example: 

The BSD 0 Clause License will be named: 0BSD.c.


There are two sets of directories for the test files:

noid   - Contains test files with the license text.
withid - Contains test files with the license text and an SPDX License Identifier (see below for link).



2.0 Versions and links


License List: https://spdx.org/licenses/ 
License List Version: 2.6 
JSON files: https://github.com/spdx/license-list-data/tree/v2.6 
SPDX License Identifiers: https://spdx.org/using-spdx#identifiers 
Github repo for the test files: https://github.com/spdx/license-test-files


3.0 Caveats

This is the first release of the test files and they have not undergone extensive testing with license scanners yet. Not all licenses will 
have a copyright. If a copyright does appear it is because it is part of the SPDX License Text or Standard Header. Some License markup 
may appear for some licenses.


4.0 Issues 

You can report issues with the test files or ask for enhancements using the GitHub repo.
