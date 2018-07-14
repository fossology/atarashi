/*
** THIS IS A TEST FILE FOR THE SPDX LICENSE DETECTION TESTS											
**																										
** This file has been auto generated using the SPDX License List as represented by
** the JSON files:  https://github.com/spdx/license-list-data 
** 
** This file is for test purposes only. It WILL NOT compile or do anything useful otherwise.
**
** Test File Version: 1.0 No SPDX Identifiers - License List version 2.6
**
** DISCLAIMER
**
** Any copyrights appearing in this test file do so because they were part of the license text as stored by SPDX and are included 
** only for test purposes as they are part of the license text.	They have no meaning, implied or specific, otherwise.	
*/




/*
** LICENSE HEADER AND COPYRIGHT TO DETECT	
** This section either uses either the standard license header, or if one does not exist, the license 
** text as shown on the SPDX License List. In addition, if the file was generated using the write 
** license identifiers option, they will appear before the license text.
** 										
**
** SPDX License to detect: https://spdx.org/licenses/Ruby.html				
*/



/* SPDX-License-Identifier: Ruby */
/*
1. You may make and give away verbatim copies of the source form of
the software without restriction, provided that you duplicate all of
the original copyright notices and associated disclaimers.

2. You may
modify your copy of the software in any way, provided that you do at
least ONE of the following:

     a) place your modifications in the
Public Domain or otherwise make them Freely Available, such as by
posting said modifications to Usenet or an equivalent medium, or by
allowing the author to include your modifications in the software.

  
  b) use the modified software only within your corporation or
organization.

     c) give non-standard binaries non-standard names,
with instructions on where to get the original software
distribution.

     d) make other distribution arrangements with the
author.

3. You may distribute the software in object code or binary
form, provided that you do at least ONE of the following:

     a)
distribute the binaries and library files of the software, together
with instructions (in the manual page or equivalent) on where to get
the original distribution.

     b) accompany the distribution with
the machine-readable source of the software.

     c) give
non-standard binaries non-standard names, with instructions on where
to get the original software distribution.

     d) make other
distribution arrangements with the author.

4. You may modify and
include the part of the software into any other software (possibly
commercial). But some files in the distribution are not written by the
author, so that they are not under these terms.

For the list of those
files and their copying conditions, see the file LEGAL.

5. The
scripts and library files supplied as input to or produced as output
from the software do not automatically fall under the copyright of the
software, but belong to whomever generated them, and may be sold
commercially, and may be aggregated with this software.

6. THIS
SOFTWARE IS PROVIDED "AS IS" AND WITHOUT ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
*/

/*
** Fake code so we have something.
*/
#include <nothing.h>


int
noop_fun(int arg1)
{
	short retval;
	
	recalculatearg(&arg1);
	
	switch (arg1)
	{
		case 0:
			if (arg1) {
					retval = 1;
			} else {
			retval = 2;
			}
		case 1:
			retval = 2;
		case 2:
			retval = morpharg(arg1);
		case 3:
			if (arg1) {
				retval = 6;
			} else {
				retval = 7;
			}
		case 4:
			retval = upscalearg(arg1);
		default:
			retval = 0;
	}
	
	return retval;
}

