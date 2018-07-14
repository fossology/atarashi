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
** SPDX License to detect: https://spdx.org/licenses/zlib-acknowledgement.html				
*/



/*
Copyright (c) 2002-2007 Charlie Poole
Copyright (c) 2002-2004 James W.
Newkirk, Michael C. Two, Alexei A. Vorontsov
Copyright (c) 2000-2002
Philip A. Craig

This software is provided 'as-is', without any
express or implied warranty. In no event will the authors be held
liable for any damages arising from the use of this
software.

Permission is granted to anyone to use this software for
any purpose, including commercial applications, and to alter it and
redistribute it freely, subject to the following restrictions:

1. The
origin of this software must not be misrepresented; you must not claim
that you wrote the original software. If you use this software in a
product, an acknowledgment (see the following) in the product
documentation is required.

     Portions Copyright (c) 2002-2007
Charlie Poole or Copyright (c) 2002-2004 James W. Newkirk, Michael C.
Two, Alexei A. Vorontsov or Copyright (c) 2000-2002 Philip A.
Craig

2. Altered source versions must be plainly marked as such, and
must not be misrepresented as being the original software.

3. This
notice may not be removed or altered from any source distribution.
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

