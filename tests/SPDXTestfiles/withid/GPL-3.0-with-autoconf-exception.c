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
** SPDX License to detect: https://spdx.org/licenses/GPL-3.0-with-autoconf-exception.html				
*/



/* SPDX-License-Identifier: GPL-3.0-with-autoconf-exception */
/*
insert GPL v3 text here

AUTOCONF CONFIGURE SCRIPT EXCEPTION

Version
3.0, 18 August 2009

Copyright © 2009 Free Software Foundation, Inc.
<http://fsf.org/>

Everyone is permitted to copy and distribute
verbatim copies of this license document, but changing it is not
allowed.

This Exception is an additional permission under section 7
of the GNU General Public License, version 3 ("GPLv3"). It applies to
a given file that bears a notice placed by the copyright holder of the
file stating that the file is governed by GPLv3 along with this
Exception.

The purpose of this Exception is to allow distribution of
Autoconf's typical output under terms of the recipient's choice
(including proprietary).

0. Definitions.
"Covered Code" is the source
or object code of a version of Autoconf that is a covered work under
this License.

"Normally Copied Code" for a version of Autoconf means
all parts of its Covered Code which that version can copy from its
code (i.e., not from its input file) into its minimally verbose,
non-debugging and non-tracing output.

"Ineligible Code" is Covered
Code that is not Normally Copied Code.

1. Grant of Additional
Permission.
You have permission to propagate output of Autoconf, even
if such propagation would otherwise violate the terms of GPLv3.
However, if by modifying Autoconf you cause any Ineligible Code of the
version you received to become Normally Copied Code of your modified
version, then you void this Exception for the resulting covered work.
If you convey that resulting covered work, you must remove this
Exception in accordance with the second paragraph of Section 7 of
GPLv3.

2. No Weakening of Autoconf Copyleft.
The availability of this
Exception does not imply any general presumption that third-party
software is unaffected by the copyleft requirements of the license of
Autoconf.
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

