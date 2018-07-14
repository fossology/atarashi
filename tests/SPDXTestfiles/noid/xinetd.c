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
** SPDX License to detect: https://spdx.org/licenses/xinetd.html				
*/



/*
ORIGINAL LICENSE: This software is

(c) Copyright 1992 by Panagiotis
Tsirigotis

The author (Panagiotis Tsirigotis) grants permission to
use, copy, and distribute this software and its documentation for any
purpose and without fee, provided that the above copyright notice
extant in files in this distribution is not removed from files
included in any redistribution and that this copyright notice is also
included in any redistribution.

Modifications to this software may be
distributed, either by distributing the modified software or by
distributing patches to the original software, under the following
additional terms:

1. The version number will be modified as follows:

     a. The first 3 components of the version number (i.e
<number>.<number>.<number>) will remain unchanged. 
     b. A new
component will be appended to the version number to indicate the
modification level. The form of this component is up to the author of
the modifications.

2. The author of the modifications will include
his/her name by appending it along with the new version number to this
file and will be responsible for any wrong behavior of the modified
software.

The author makes no representations about the suitability
of this software for any purpose. It is provided "as is" without any
express or implied warranty. 

Modifications: Version: 2.1.8.7-current
Copyright 1998-2001 by Rob Braun

Sensor Addition Version:
2.1.8.9pre14a Copyright 2001 by Steve Grubb

This is an exerpt from an
email I recieved from the original author, allowing xinetd as
maintained by me (Rob Braun), to use the higher version numbers:

I
appreciate your maintaining the version string guidelines as specified
in the copyright. But I did not mean them to last as long as they
did.

So, if you want, you may use any 2.N.* (N >= 3) version string
for future xinetd versions that you release. Note that I am excluding
the 2.2.* line; using that would only create confusion. Naming the
next release 2.3.0 would put to rest the confusion about 2.2.1 and
2.1.8.*.
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

