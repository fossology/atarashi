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
** SPDX License to detect: https://spdx.org/licenses/Watcom-1.0.html				
*/



/* SPDX-License-Identifier: Watcom-1.0 */
/*
Portions Copyright (c) 1983-2002 Sybase, Inc. All Rights
Reserved.
This file contains Original Code and/or Modifications of
Original Code as defined in and that are subject to the Sybase Open
Watcom Public License version 1.0 (the 'License'). You may not use
this file except in compliance with the License. BY USING THIS FILE
YOU AGREE TO ALL TERMS AND CONDITIONS OF THE LICENSE. A copy of the
License is provided with the Original Code and Modifications, and is
also available at www.sybase.com/developer/opensource. 

The Original
Code and all software distributed under the License are distributed on
an 'AS IS' basis, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR
IMPLIED, AND SYBASE AND ALL CONTRIBUTORS HEREBY DISCLAIM ALL SUCH
WARRANTIES, INCLUDING WITHOUT LIMITATION, ANY WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, QUIET ENJOYMENT OR
NON-INFRINGEMENT. Please see the License for the specific language
governing rights and limitations under the License."
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

