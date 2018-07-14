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
** SPDX License to detect: https://spdx.org/licenses/Spencer-94.html				
*/



/* SPDX-License-Identifier: Spencer-94 */
/*
Copyright 1992, 1993, 1994 Henry Spencer.  All rights reserved.
This
software is not subject to any license of the American Telephone and
Telegraph Company or of the Regents of the University of
California.

Permission is granted to anyone to use this software for
any purpose on any computer system, and to alter it and redistribute
it, subject to the following restrictions:

1. The author is not
responsible for the consequences of use of this software, no matter
how awful, even if they arise from flaws in it.

2. The origin of this
software must not be misrepresented, either by explicit claim or by
omission.  Since few users ever read sources, credits must appear in
the documentation.

3. Altered versions must be plainly marked as
such, and must not be misrepresented as being the original software. 
Since few users ever read sources, credits must appear in the
documentation.

4. This notice may not be removed or altered.
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

