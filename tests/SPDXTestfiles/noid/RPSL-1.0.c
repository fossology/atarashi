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
** SPDX License to detect: https://spdx.org/licenses/RPSL-1.0.html				
*/



/*
Copyright © 1995-2002 RealNetworks, Inc. and/or its licensors. All
Rights Reserved.

The contents of this file, and the files included
with this file, are subject to the current version of the RealNetworks
Public Source License Version 1.0 (the "RPSL") available at
https://www.helixcommunity.org/content/rpsl unless you have licensed
the file under the RealNetworks Community Source License Version 1.0
(the "RCSL") available at https://www.helixcommunity.org/content/rcsl,
in which case the RCSL will apply. You may also obtain the license
terms directly from RealNetworks. You may not use this file except in
compliance with the RPSL or, if you have a valid RCSL with
RealNetworks applicable to this file, the RCSL. Please see the
applicable RPSL or RCSL for the rights, obligations and limitations
governing use of the contents of the file.

This file is part of the
Helix DNA Technology. RealNetworks is the developer of the Original
code and owns the copyrights in the portions it created.

This file,
and the files included with this file, is distributed and made
available on an 'AS IS' basis, WITHOUT WARRANTY OF ANY KIND, EITHER
EXPRESS OR IMPLIED, AND REALNETWORKS HEREBY DISCLAIMS ALL SUCH
WARRANTIES, INCLUDING WITHOUT LIMITATION, ANY WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, QUIET ENJOYMENT OR
NON-INFRINGEMENT.

Contributor(s):
<<var;name=contributor;original=_____;match=.+>>

Technology
Compatibility Kit Test Suite(s) Location (if licensed under the
RCSL):
<<var;name=testLocation;original=_____;match=.+>>.
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

