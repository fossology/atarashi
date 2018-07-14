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
** SPDX License to detect: https://spdx.org/licenses/SGI-B-1.1.html				
*/



/* SPDX-License-Identifier: SGI-B-1.1 */
/*
License Applicability. Except to the extent portions of this file are
made subject to an alternative license as permitted in the SGI Free
Software License B, Version 1.1 (the "License"), the contents of this
file are subject only to the provisions of the License. You may not
use this file except in compliance with the License. You may obtain a
copy of the License at Silicon Graphics, Inc., attn: Legal Services,
1600 Amphitheatre Parkway, Mountain View, CA 94043-1351, or at:


http://oss.sgi.com/projects/FreeB

Note that, as provided in the
License, the Software is distributed on an "AS IS" basis, with ALL
EXPRESS AND IMPLIED WARRANTIES AND CONDITIONS DISCLAIMED, INCLUDING,
WITHOUT LIMITATION, ANY IMPLIED WARRANTIES AND CONDITIONS OF
MERCHANTABILITY, SATISFACTORY QUALITY, FITNESS FOR A PARTICULAR
PURPOSE, AND NON-INFRINGEMENT.

Original Code. The Original Code is:
[name of software, version number, and release date], developed by
Silicon Graphics, Inc. The Original Code is Copyright (c) [dates of
first publication, as appearing in the Notice in the Original Code]
Silicon Graphics, Inc. Copyright in any portions created by third
parties is as indicated elsewhere herein. All Rights Reserved.
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

