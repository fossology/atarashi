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
** SPDX License to detect: https://spdx.org/licenses/gnuplot.html				
*/



/*
Copyright 1986 - 1993, 1998, 2004 Thomas Williams, Colin
Kelley

Permission to use, copy, and distribute this software and its
documentation for any purpose with or without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation.

Permission to modify the software is
granted, but not the right to distribute the complete modified source
code. Modifications are to be distributed as patches to the released
version. Permission to distribute binaries produced by compiling
modified sources is granted, provided you 

     1. distribute the
corresponding source modifications from the released version in the
form of a patch file along with the binaries, 
     2. add special
version identification to distinguish your version in addition to the
base release version number, 
     3. provide your name and address as
the primary contact for the support of your modified version, and 
   
 4. retain our contact information in regard to use of the base
software. 

Permission to distribute the released version of the
source code along with corresponding source modifications in the form
of a patch file is granted with same provisions 2 through 4 for binary
distributions.

This software is provided "as is" without express or
implied warranty to the extent permitted by applicable law.
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

